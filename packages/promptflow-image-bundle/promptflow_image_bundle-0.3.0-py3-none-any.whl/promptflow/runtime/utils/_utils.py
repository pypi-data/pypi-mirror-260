# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import base64
import contextlib
import json
import logging
import os
import sys
import traceback
import zlib
from contextvars import ContextVar
from functools import lru_cache

from azure.identity import DefaultAzureCredential

from promptflow._internal import (
    VERSION,
    CredentialScrubberFormatter,
    ExceptionPresenter,
    FileHandlerConcurrentWrapper,
    JsonSerializedPromptflowException,
)
from promptflow.contracts.run_mode import RunMode
from promptflow.runtime.constants import ENV_AZURE_ACTIVE_DIRECTORY, ENV_AZURE_RESOURCE_MANAGER
from promptflow.runtime.contracts.azure_storage_setting import AzureStorageSetting
from promptflow.runtime.utils.internal_logger_utils import TelemetryLogHandler

PF_LOGGING_LEVEL = "PF_LOGGING_LEVEL"
FORMATTER = CredentialScrubberFormatter(
    fmt="[%(asctime)s]  [%(process)d] %(name)-8s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(
    logger_name,
    log_level: int = logging.NOTSET,
    std_out: bool = False,
    log_formatter: logging.Formatter = None,
) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    log_level = get_logging_level(log_level)
    logger.setLevel(log_level)
    if std_out:
        fh = logging.StreamHandler(sys.stderr)
        if log_formatter:
            fh.setFormatter(log_formatter)
        logger.addHandler(fh)
    logger.addHandler(FileHandlerConcurrentWrapper())
    logger.addHandler(TelemetryLogHandler.get_instance())
    return logger


def get_logging_level(level: int = logging.NOTSET, envs: dict[str, str] = None) -> int:
    """Get logging level.

    If level is set explicitly, return it.
    Otherwise, try to get level from environment variable, or default INFO level if not exists.
    """
    if level == logging.NOTSET:
        if envs is not None and PF_LOGGING_LEVEL in envs:
            level = envs[PF_LOGGING_LEVEL].strip().upper()
            # convert to int level, and default to INFO if invalid
            level = logging._nameToLevel.get(level, logging.INFO)
        elif os.getenv(PF_LOGGING_LEVEL) is not None:
            level = os.getenv(PF_LOGGING_LEVEL).strip().upper()
            level = logging._nameToLevel.get(level, logging.INFO)
        else:
            level = logging.INFO
    return level


def is_in_ci_pipeline():
    if os.environ.get("IS_IN_CI_PIPELINE") == "true":
        return True
    return False


def decode_dict(data: str) -> dict:
    # str -> bytes
    data = data.encode()
    zipped_conns = base64.b64decode(data)
    # gzip decode
    conns_data = zlib.decompress(zipped_conns, 16 + zlib.MAX_WBITS)
    return json.loads(conns_data.decode())


def encode_dict(data: dict) -> str:
    # json encode
    data = json.dumps(data)
    # gzip compress
    gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
    zipped_data = gzip_compress.compress(data.encode()) + gzip_compress.flush()
    # base64 encode
    b64_data = base64.b64encode(zipped_data)
    # bytes -> str
    return b64_data.decode()


def get_value_by_key_path(dct, key_path, default_value=None):
    """Given a dict, get value from key path.

    >>> dct = {
    ...     'Beijing': {
    ...         'Haidian': {
    ...             'ZipCode': '110108',
    ...         }
    ...     }
    ... }
    >>> get_value_by_key_path(dct, 'Beijing/Haidian/ZipCode')
    '110108'
    """
    if not key_path:
        raise ValueError("key_path must not be empty")

    segments = key_path.split("/")
    final_flag = object()
    segments.append(final_flag)

    walked = []

    cur_obj = dct
    for seg in segments:
        # If current segment is final_flag,
        # the cur_obj is the object that the given key path points to.
        # Simply return it as result.
        if seg is final_flag:
            # return default_value if cur_obj is None
            return default_value if cur_obj is None else cur_obj

        # If still in the middle of key path, when cur_obj is not a dict,
        # will fail to locate the values, so return default_value if not found.
        if not isinstance(cur_obj, dict):
            return default_value

        # Move to next segment
        cur_obj = cur_obj.get(seg)
        walked.append(seg)

    raise Exception(f"Failed to get value by key path: {key_path}")


def get_string_size(content: str) -> int:
    """Get the size of content"""
    return len(content.encode("utf-8"))


def get_mlflow_tracking_uri(
    subscription_id: str, resource_group_name: str, workspace_name: str, mt_endpoint: str
) -> str:
    """Get the full mlflow tracking uri"""
    # "https://master.api.azureml-test.ms" to "azureml://master.api.azureml-test.ms"
    return (
        f"{mt_endpoint.replace('https', 'azureml')}/mlflow/v1.0/subscriptions/{subscription_id}/"
        f"resourceGroups/{resource_group_name}/providers/Microsoft.MachineLearningServices/workspaces/{workspace_name}"
    )


def get_default_credential():  # move
    """get default credential for current compute, cache the result to minimize actual token request count sent"""
    if is_in_ci_pipeline():
        from azure.identity import AzureCliCredential

        cred = AzureCliCredential()
    else:
        cred = get_default_azure_credential()
    return cred


def get_default_azure_credential():
    """Get DefaultAzureCredential for public/sovereign/airgapped clouds."""
    # If has AZURE_ACTIVE_DIRECTORY environment variable, set it as auth authority.
    if os.environ.get(ENV_AZURE_ACTIVE_DIRECTORY) is not None:
        authority = os.environ[ENV_AZURE_ACTIVE_DIRECTORY]
        return DefaultAzureCredential(authority=authority, exclude_interactive_browser_credential=True)
    # use default AZURE_PUBLIC_CLOUD authority.
    else:
        return DefaultAzureCredential(exclude_interactive_browser_credential=True)


def get_resource_management_scope():
    """Get the resource management scope for public/sovereign/airgapped clouds."""
    # if has AZURE_RESOURCE_MANAGER environment variable, use it as scope.
    if os.environ.get(ENV_AZURE_RESOURCE_MANAGER) is not None:
        return f"{os.environ[ENV_AZURE_RESOURCE_MANAGER].rstrip('/')}/.default"
    # use default management scope.
    else:
        return "https://management.azure.com/.default"


def get_runtime_version():
    build_info = os.environ.get("BUILD_INFO", "")
    try:
        build_info_dict = json.loads(build_info)
        return build_info_dict["build_number"]
    except Exception:
        return "unknown"


def log_runtime_pf_version(logger):
    version = get_runtime_version()
    if version is not None and version != "unknown":
        logger.info(f"Runtime version: {version}. PromptFlow version: {VERSION}")
    else:
        logger.info(f"PromptFlow version: {VERSION}")


@contextlib.contextmanager
def multi_processing_exception_wrapper(exception_queue):
    """Wrap the exception to a generic exception to avoid the pickle error."""
    try:
        yield
    except Exception as e:
        # func runs in a child process, any customized exception can't have extra arguments other than message
        # wrap the exception to a generic exception to avoid the pickle error
        # Ref: https://bugs.python.org/issue32696
        exception_dict = ExceptionPresenter.create(e).to_dict(include_debug_info=True)
        message = json.dumps(exception_dict)
        exception = JsonSerializedPromptflowException(message=message)
        exception_queue.put(exception)
        raise exception from e


@lru_cache
def get_storage_from_config(
    config,
    token=None,
    azure_storage_setting: AzureStorageSetting = None,
    run_mode: RunMode = None,
):
    return config.get_run_storage(
        workspace_access_token=token, azure_storage_setting=azure_storage_setting, run_mode=run_mode
    )


@lru_cache
def get_workspace_config(ml_client, logger):
    """Get workspace config from ml_client. Returns empty dict if failed to get config."""
    try:
        ws = ml_client.workspaces.get()
        worspace_rest = ml_client.workspaces._operation.get(
            resource_group_name=ml_client.resource_group_name, workspace_name=ml_client.workspace_name
        )

        return {
            "storage_account": ws.storage_account.split("/")[-1],
            "mt_service_endpoint": ws.discovery_url.replace("/discovery", ""),
            "resource_group": ws.resource_group,
            "subscription_id": ml_client.subscription_id,
            "workspace_name": ws.name,
            "workspace_id": worspace_rest.workspace_id,
        }
    except Exception as ex:
        logger.warning(f"Failed to get default config from ml_client: {ex}")
        logger.warning(traceback.format_exc())
        return {}


@contextlib.contextmanager
def setup_contextvar(contextvar: ContextVar, value):
    token = contextvar.set(value)
    try:
        yield
    finally:
        contextvar.reset(token)
