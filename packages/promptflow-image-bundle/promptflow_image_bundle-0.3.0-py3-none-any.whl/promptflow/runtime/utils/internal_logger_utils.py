# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# This file is not for open source.


import logging
import re
import sys
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from enum import Enum
from functools import partial
from io import TextIOWrapper
from threading import RLock
from typing import Dict, List, Optional

from azure.storage.blob import BlobClient
from opencensus.ext.azure.log_exporter import AzureLogHandler

from promptflow._internal import (
    DATETIME_FORMAT,
    LOG_FORMAT,
    CredentialScrubber,
    CredentialScrubberFormatter,
    ErrorResponse,
    FileHandler,
    FileHandlerConcurrentWrapper,
    LogContext,
)
from promptflow.contracts.run_mode import RunMode
from promptflow.runtime.utils._debug_log_helper import generate_safe_error_stacktrace


@contextmanager
def disable_logging():
    """
    A context manager that will prevent any logging messages.
    """
    previous_level = logging.root.manager.disable

    logging.disable(logging.CRITICAL + 1)

    try:
        yield
    finally:
        logging.disable(previous_level)


class BlobStream(TextIOWrapper):
    def __init__(self, sas_uri: str, raise_exception=False):
        self._raise_exception = raise_exception
        try:
            self._blob_client = BlobClient.from_blob_url(sas_uri)
        except Exception as ex:
            logging.exception(f"Failed to create blob client from sas uri. Exception: {ex}")
            if raise_exception:
                raise

    def write(self, s: str):
        """Override TextIOWrapper's write method."""
        # Disable logging when uploading log to blob, otherwise might encounter deadloop.
        with disable_logging():
            try:
                self._blob_client.upload_blob(s, blob_type="AppendBlob")
            except Exception:
                if self._raise_exception:
                    raise

    def flush(self):
        """Override TextIOWrapper's flush method."""
        pass


class BlobFileHandler(FileHandler):
    """Write compliant log to a blob file in azure storage account."""

    STDERR_PATTERN = " (index starts from 0)] stderr> "
    ERR_SCRUBBED_TEXT = "**Error message scrubbed**"

    def __init__(self, file_path: str, log_filtering_patterns: List[str] = None):
        self._log_filtering_patterns = log_filtering_patterns
        if self._log_filtering_patterns:
            """
            If log_filtering_patterns is set, then use CustomerContentScrubberFormatter to scrub customer content.
            """
            super().__init__(file_path, CustomerContentScrubberFormatter(fmt=LOG_FORMAT, datefmt=DATETIME_FORMAT))
        else:
            super().__init__(file_path)

    def _get_stream_handler(self, file_path: str) -> logging.StreamHandler:
        """Override FileHandler's _get_stream_handler method."""
        return logging.StreamHandler(BlobStream(file_path))

    def emit(self, record: logging.LogRecord):
        """
        Override FileHandler's emit method.

        If no log_filtering_patterns is set, then log as usual.
        If log_filtering_patterns is set,
        - Not log error message to blob file.
        - Do pattern match for std err log
        """
        if not self._log_filtering_patterns:
            return super().emit(record)

        if record.levelno == logging.ERROR:
            record.msg = "**Error message scrubbed**"
            return super().emit(record)

        if self.should_log_with_filter_pattern(record):
            return super().emit(record)

    def should_log_with_filter_pattern(self, record: logging.LogRecord):
        """
        Check if the log should be logged to blob file.
        std err example: WARNING  [echo in line 9 (index starts from 0)] stderr> SystemLog: will output data

        - Check if is warning log, if not, the log is not std err log, then log it.
        - Check if the log contains stderr pattern, if not, the log is not std err log, then log it.
        - Check if the log matches any pattern in log_filtering_patterns, if yes, then do log it.
        - If not match any pattern, then do not log it.
        """
        if record.levelno != logging.WARNING:
            return True

        message = record.getMessage()
        pre_index = message.find(self.STDERR_PATTERN)
        if pre_index == -1:
            return True

        # if found, its stderr log
        err_conent = message[pre_index + len(self.STDERR_PATTERN) :]

        for pattern in self._log_filtering_patterns:
            if re.match(pattern, err_conent):
                return True

        return False


class FileType(Enum):
    Local = "Local"
    Blob = "Blob"


@dataclass
class SystemLogContext(LogContext):
    file_type: Optional[FileType] = FileType.Local
    # TODO: Remove instrumentation_key because it is already been set from request header.
    app_insights_instrumentation_key: Optional[str] = None  # If set, logs will also be sent to app insights.
    custom_dimensions: Optional[Dict[str, str]] = None  # Custom dimension column in app insight log.
    log_filtering_patterns: List[str] = None  # Log filter apply for the logger

    def get_initializer(self):
        return partial(
            SystemLogContext,
            file_path=self.file_path,
            run_mode=self.run_mode,
            credential_list=self.credential_list,
            file_type=self.file_type,
            app_insights_instrumentation_key=self.app_insights_instrumentation_key,
            log_filtering_patterns=self.log_filtering_patterns,
            custom_dimensions=self.custom_dimensions,
        )

    def __enter__(self):
        self.loggers = [system_logger]
        # Set connection string and customer dimensions for telemetry log handler.
        if self.input_logger:
            self.loggers.append(self.input_logger)
        for logger in self.loggers:
            for log_handler in logger.handlers:
                if isinstance(log_handler, TelemetryLogHandler):
                    log_handler.set_connection_string(self.app_insights_instrumentation_key)
                    log_handler.set_or_update_context(self.custom_dimensions)
                    log_handler.set_credential_list(self.credential_list or [])

        super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        # Flush telemetry log handler.
        for logger in self.loggers:
            for log_handler in logger.handlers:
                if isinstance(log_handler, TelemetryLogHandler):
                    log_handler.flush()

    def _set_log_path(self):
        """Override _set_log_path of parent class."""
        if not self.file_path:
            return

        if self.file_type == FileType.Local:
            super()._set_log_path()
        elif self.file_type == FileType.Blob:
            logger_list = self._get_loggers_to_set_path()
            for logger_ in logger_list:
                for log_handler in logger_.handlers:
                    if isinstance(log_handler, FileHandlerConcurrentWrapper):
                        # Only need to do scrub for execution logger.
                        # For the test run, the submitter owns the data, there is no risk of data leak.
                        if (
                            (self.run_mode == RunMode.Batch)
                            and (self.log_filtering_patterns)
                            and (logger_.name == "execution")
                        ):
                            log_handler.handler = BlobFileHandler(
                                self.file_path, log_filtering_patterns=self.log_filtering_patterns
                            )
                        else:
                            log_handler.handler = BlobFileHandler(self.file_path)
        else:
            raise ValueError(f"Unsupported file type {self.file_type}.")


@contextmanager
def set_custom_dimensions_to_logger(input_logger: logging.Logger, custom_dimensions: Dict[str, str]):
    for handler in input_logger.handlers:
        if isinstance(handler, TelemetryLogHandler):
            handler.set_or_update_context(custom_dimensions)
    try:
        yield
    finally:
        for handler in input_logger.handlers:
            if isinstance(handler, TelemetryLogHandler):
                handler.flush()


class CustomerContentScrubberFormatter(CredentialScrubberFormatter):
    """Formatter that scrubs credential and customer content in logs."""

    def _handle_customer_content(self, s: str, record: logging.LogRecord) -> str:
        """Override CredentialScrubberFormatter's _handle_customer_content method.

        Replace "{customer_content}" in log message with compliant exception info or **data_scrubed**.
        """
        # If log record does not have "customer_content" field, return input logging string directly.
        if not hasattr(record, "customer_content"):
            return s

        customer_content = record.customer_content
        # If customer_content is an exception, convert it to a compliant string without customer content,
        # then replace {customer_content} with the string.
        if isinstance(customer_content, Exception):
            ex_s = self._convert_exception_to_str(customer_content)
            return s.replace("{customer_content}", ex_s)

        return s.replace("{customer_content}", CredentialScrubber.PLACE_HOLDER)

    def _handle_traceback(self, s: str, record: logging.LogRecord) -> str:
        """Override CredentialScrubberFormatter's _handle_traceback method.

        Handle traceback part in log message.
        """
        if record.levelno >= logging.ERROR:
            # Scrub everything after traceback, because it might contain customer information.
            return re.sub(r"\s*traceback.*", "", s, flags=re.IGNORECASE | re.DOTALL)
        return s

    def _convert_exception_to_str(self, ex: Exception) -> str:
        """Override CredentialScrubberFormatter's _convert_exception_to_str method."""
        try:
            error_response_dict = ErrorResponse.from_exception(ex, include_debug_info=True).to_dict()
            stack_trace = generate_safe_error_stacktrace(error_response_dict)
        except:  # noqa: E722
            stack_trace = ""
        s = f"Exception type: {ex.__class__.__name__}.\nDebug info: {stack_trace}"
        return s


class TelemetryLogHandler(logging.Handler):
    """Write compliant log (no customer content) to app insights."""

    FORMAT = "%(message)s"
    CONNECTION_STRING = ""
    SINGLE_LOCK = RLock()

    def __init__(self):
        super().__init__()
        self._handler = None
        self._context = ContextVar("request_context", default=None)
        self._formatter = CustomerContentScrubberFormatter(fmt=self.FORMAT)

    @classmethod
    def get_instance(cls):
        with TelemetryLogHandler.SINGLE_LOCK:
            if not hasattr(TelemetryLogHandler, "_singleton"):
                TelemetryLogHandler._singleton = TelemetryLogHandler()
        return TelemetryLogHandler._singleton

    def set_connection_string(self, connection_string: Optional[str]):
        """Set connection string and azure log handler."""
        if not connection_string:
            return

        # If connection string is set already, then do not set again.
        if TelemetryLogHandler.CONNECTION_STRING == connection_string:
            return

        TelemetryLogHandler.CONNECTION_STRING = connection_string
        handler = AzureLogHandler(connection_string=connection_string)
        handler.setFormatter(self._formatter)
        self._handler = handler

    def set_or_update_context(self, context: Optional[Dict[str, str]]):
        """Set log context, such as request id, workspace info."""
        if context is None:
            return

        current_context: Dict = self._context.get()
        if current_context is None:
            self._context.set(context)
        else:
            current_context.update(context)

    def set_credential_list(self, credential_list: List[str]):
        """Set credential list, which will be scrubbed in logs."""
        self._formatter.set_credential_list(credential_list)

    def emit(self, record: logging.LogRecord):
        """Override logging.Handler's emit method."""
        if not self._handler:
            return

        # If the whole message is to be scrubbed, then do not emit.
        if self._formatter.format(record) == CredentialScrubber.PLACE_HOLDER:
            return

        # Add custom_dimensions to record
        record.custom_dimensions = self._get_custom_dimensions(record)
        # Set exc_info to None, otherwise this log will be sent to app insights's exception table.
        record.exc_info = None
        self._handler.emit(record)

    def reset_log_handler(self):
        """Reset handler."""
        if not TelemetryLogHandler.CONNECTION_STRING:
            return

        if self._handler:
            self._handler.flush()

        self._handler = AzureLogHandler(connection_string=TelemetryLogHandler.CONNECTION_STRING)
        self._handler.setFormatter(self._formatter)

    def close(self):
        """Close log handler."""
        if self._handler is None:
            return
        self._handler.close()

    def clear(self):
        """Clear context variable."""
        self._context.set(None)
        self._formatter.clear()

    def flush(self):
        """Flush log."""
        if self._handler is None:
            return
        self._handler.flush()

    def _get_custom_dimensions(self, record: logging.LogRecord) -> Dict[str, str]:
        custom_dimensions = self._context.get()
        if not custom_dimensions:
            custom_dimensions = dict()

        if hasattr(record, "custom_dimensions"):
            custom_dimensions.update(record.custom_dimensions)

        custom_dimensions.update(
            {
                "processId": record.process,
                "name": record.name,
            }
        )
        return custom_dimensions


def reset_telemetry_log_handler(input_logger: logging.Logger):
    for handler in input_logger.handlers:
        if isinstance(handler, TelemetryLogHandler):
            handler.reset_log_handler()


def close_telemetry_log_handler(input_logger: logging.Logger):
    for handler in input_logger.handlers:
        if isinstance(handler, TelemetryLogHandler):
            handler.close()


def _get_system_logger(
    logger_name,
    log_level: int = logging.DEBUG,
) -> logging.Logger:
    logger = logging.Logger(logger_name)
    logger.setLevel(log_level)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(CustomerContentScrubberFormatter(fmt=LOG_FORMAT, datefmt=DATETIME_FORMAT))
    logger.addHandler(stdout_handler)
    logger.addHandler(TelemetryLogHandler.get_instance())
    return logger


def set_app_insights_instrumentation_key(instrumentation_key: str):
    TelemetryLogHandler.get_instance().set_connection_string(instrumentation_key)


# The system_logger will only capture logs in app insights, which will remain hidden from customers' view.
system_logger = _get_system_logger("promptflow-system")
