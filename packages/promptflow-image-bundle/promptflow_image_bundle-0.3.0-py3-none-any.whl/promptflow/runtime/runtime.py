# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import contextvars
import json
import multiprocessing
import os
import re
import shutil
import signal
import threading
import time
import uuid
from contextlib import contextmanager
from datetime import timedelta
from pathlib import Path
from tempfile import gettempdir
from typing import Callable, Dict, List, Union

import psutil
from azure.core.exceptions import ClientAuthenticationError
from psutil import NoSuchProcess

from promptflow._internal import (
    VERSION,
    ConnectionManager,
    DefaultRunStorage,
    ErrorResponse,
    ExceptionPresenter,
    JsonSerializedPromptflowException,
    OperationContext,
    apply_inputs_mapping,
    get_feature_list,
    set_context,
)
from promptflow._utils.credential_scrubber import CredentialScrubber
from promptflow.batch import BatchEngine
from promptflow.batch._result import BatchResult
from promptflow.contracts.flow import Flow, FlowInputAssignment
from promptflow.contracts.run_info import FlowRunInfo, RunInfo, Status
from promptflow.executor.flow_executor import FlowExecutor
from promptflow.runtime._errors import FlowFileNotFound, InvalidAssetId, UserAuthenticationError
from promptflow.runtime.constants import ComputeType, PromptflowEdition
from promptflow.runtime.contracts.runtime import (
    AsyncFlowRequest,
    AsyncSingleNodeRequest,
    BulkRunRequestV2,
    CancelRunRequest,
    FlowRequestV2,
    FlowSourceType,
    SingleNodeRequestV2,
    SubmissionRequestBaseV2,
)
from promptflow.runtime.csharp_executor_proxy import CSharpExecutorProxy
from promptflow.runtime.executor_image_manager import HOST_MOUNT_PATH
from promptflow.runtime.storage.async_run_storage import AsyncRunStorage
from promptflow.runtime.storage.azureml_run_storage_v2 import AzureMLRunStorageV2
from promptflow.runtime.utils._run_history_client import RunHistoryClient
from promptflow.runtime.utils._str_utils import join_stripped
from promptflow.runtime.utils._utils import get_runtime_version
from promptflow.runtime.utils.internal_logger_utils import (
    FileType,
    SystemLogContext,
    close_telemetry_log_handler,
    reset_telemetry_log_handler,
    system_logger,
)
from promptflow.runtime.utils.mlflow_helper import MlflowHelper, generate_error_dict_for_root_run
from promptflow.runtime.utils.multimedia_data_converter import convert_url_to_path
from promptflow.runtime.utils.progress_timer import ProgressTimer
from promptflow.runtime.utils.retry_utils import retry
from promptflow.runtime.utils.thread_utils import timeout

from ._errors import (
    DataInputsNotfound,
    FlowRunTimeoutError,
    InvalidClientAuthentication,
    InvalidDataInputs,
    UnexpectedFlowSourceType,
    UnexpectedOutputSubDir,
)
from .connections import (
    build_connection_dict,
    get_used_connection_names_from_environment_variables,
    update_environment_variables_with_connections,
)
from .data import prepare_data
from .runtime_config import RuntimeConfig, load_runtime_config
from .utils import log_runtime_pf_version, logger, multi_processing_exception_wrapper
from .utils._flow_source_helper import fill_working_dir
from .utils._run_status_helper import mark_run_v2_as_failed_in_runhistory
from .utils.downloader import _get_last_part_of_uri

MAX_ROWS_COUNT = 1000
STATUS_CHECKER_INTERVAL = 20  # seconds
MONITOR_REQUEST_TIMEOUT = 10  # seconds
SYNC_SUBMISSION_TIMEOUT = 330  # seconds
WAIT_SUBPROCESS_EXCEPTION_TIMEOUT = 10  # seconds
BULKRUN_SUBMISSION_TIMEOUT = timedelta(days=10).total_seconds()
ASYNC_RUN_SUBMISSION_TIMEOUT = timedelta(days=1).total_seconds()
ASYNC_RUN_STATUS_CHECKER_INTERVAL = 5  # seconds

BatchEngine.register_executor("csharp", CSharpExecutorProxy)


class PromptFlowRuntime:
    """PromptFlow runtime."""

    _instance = None

    def __init__(self, config: RuntimeConfig):
        self.config = config

    def execute_flow(self, request: SubmissionRequestBaseV2, execute_flow_func: Callable):
        if self.config.execution.execute_in_process:
            result = execute_flow_func(self.config, request)
        else:
            result = execute_flow_request_multiprocessing(self.config, request, execute_flow_func)
        return result

    def mark_flow_runs_v2_as_failed(self, flow_request: BulkRunRequestV2, payload: dict, ex: Exception):
        try:
            code = None
            if isinstance(ex, JsonSerializedPromptflowException):
                error_dict = json.loads(ex.message)
                code = ErrorResponse.from_error_dict(error_dict).innermost_error_code
                logger.info(f"JsonSerializedPromptflowException inner most error code is:{code}.")
            else:
                code = ErrorResponse.from_exception(ex).innermost_error_code
                logger.info(f"Exception innermost_error_code is:{code}.")

            if flow_request:
                flow_run_id = flow_request.flow_run_id
            else:
                flow_run_id = payload.get("flow_run_id", "")
            if code == UserAuthenticationError.__name__:
                logger.warning("For UserAuthenticationError, cannot update run status in run history, so do nothing.")
            else:
                logger.info("For other error, try to mark job as failed in run history.")
                mark_run_v2_as_failed_in_runhistory(self.config, flow_run_id, ex)
        except Exception as exception:
            logger.warning(
                "Hit exception when mark flow runs v2 as failed: \n%s", ExceptionPresenter.create(exception).to_dict()
            )

    def update_operation_context(self, request):
        """Update operation context."""
        # Get the request id from the headers
        req_id = request.headers.get("x-ms-client-request-id") or request.headers.get("x-request-id")

        # Get the user agent from the headers and append the runtime version
        user_agent = request.headers.get("User-Agent", "")
        runtime_user_agent = join_stripped(f"promptflow-runtime/{get_runtime_version()}", user_agent)

        # Get the operation context instance and set its attributes
        operation_context = OperationContext.get_instance()
        operation_context.append_user_agent(runtime_user_agent)
        operation_context.request_id = req_id
        operation_context.runtime_version = get_runtime_version()

        # Update operation context with deployment information
        runtime_context = self.config.deployment.to_logsafe_dict()
        operation_context.update(runtime_context)

        # Update tracking keys to make sure these values are put in aoai headers
        # Not all the values in deployment_dict are put in aoai headers after this change:
        # https://github.com/microsoft/promptflow/pull/1909
        # The keys are decided according to the document:
        # https://msdata.visualstudio.com/Vienna/_git/PromptFlow?path=/docs/http_headers_for_external_services.md&version=GBmain&_a=preview
        runtime_tracking_keys = {
            "request_id",
            "runtime_version",
            # Note that resource_group and workspace_name are not included
            # since they can be non-ascii characters and cause encoding issues.
            "subscription_id",
            "workspace_id",
            # TODO: Revisit the tracking keys to make sure only required keys are added.
            "edition",
            "compute_type",
            "runtime_mode",
            "runtime_name",
            "deployment_name",
            "endpoint_name",
        }
        if hasattr(OperationContext, "_TRACKING_KEYS"):
            tracking_keys: set = operation_context.get(OperationContext._TRACKING_KEYS)
            if isinstance(tracking_keys, set):
                tracking_keys.update(runtime_tracking_keys)

    @classmethod
    def get_instance(cls):
        """get singleton instance."""
        if cls._instance is None:
            cls._instance = PromptFlowRuntime(load_runtime_config())
        return cls._instance

    @classmethod
    def init(cls, config: RuntimeConfig):
        """init runtime with config."""

        cls._instance = PromptFlowRuntime(config)


def load_and_apply_env_variables(
    dag_file: Path, working_dir=None, environment_variables_overrides: Dict[str, str] = None
):
    # https://github.com/microsoft/promptflow/pull/1451
    # This is a breaking change for Flow class.
    # For compatibility with pf packages 1.2.0 and lower version, we added this judgment logic.
    # TODO Remove this judgment logic after promptflow >= 1.3.0 is released,
    # and lower versions are no longer in use by users.
    environment_variables = environment_variables_overrides
    if hasattr(Flow, "load_env_variables"):
        environment_variables = Flow.load_env_variables(
            dag_file, working_dir=working_dir, environment_variables_overrides=environment_variables
        )
    else:
        logger.info(
            f"To configure environment variables in flow yaml, please use promptflow>=1.3.0. "
            f"The current promptflow version is {VERSION}, which does not support this feature. "
        )
    set_environment_variables(environment_variables)


def set_environment_variables(env_vars: dict):
    """set environment variables."""
    if env_vars:
        for key, value in env_vars.items():
            os.environ[key] = value


def execute_flow_request_multiprocessing_impl(
    execute_flow_func: Callable,
    config: RuntimeConfig,
    parent_pid: int,
    request: SubmissionRequestBaseV2,
    return_dict,
    exception_queue,
    context_dict: Dict,
):
    """execute flow request V2 in a child process.
    the child process should execute inside multi_processing_exception_wrapper to avoide exception issue.
    """
    # Always use "fork" method to start subprocess when executing.
    multiprocessing.set_start_method("fork", force=True)
    operation_context = OperationContext.get_instance()
    operation_context.update(context_dict)
    with multi_processing_exception_wrapper(exception_queue):
        # set log context here;
        # otherwise the previously set context-local log handlers/filters will be lost
        # because this method is invoked in another process.
        with reset_and_close_logger(), get_log_context_from_v2_request(request):
            logger.info("[%s--%s] Start processing flowV2......", parent_pid, os.getpid())
            log_runtime_pf_version(logger)
            result = execute_flow_func(config, request)
            return_dict["result"] = result


def get_multiprocessing_context() -> "multiprocessing.context.BaseContext":
    # Use "spawn" method to start child process (in linux system the default method is "fork").
    # By using "spawn" method, the child process is started with a fresh python interpreter,
    # so that all the packages will be imported again.
    # This is because package version in current environment might change (because pip install is executed)
    # after runtime is started. We need to use the freshly-installed package to start execution.
    logger.info("Use spawn method to start child process.")
    return multiprocessing.get_context("spawn")


def execute_flow_request_multiprocessing(
    config: RuntimeConfig,
    request: SubmissionRequestBaseV2,
    execute_flow_func: Callable,
):
    """execute request in a child process."""
    pid = os.getpid()
    mp = get_multiprocessing_context()
    manager = mp.Manager()
    return_dict = manager.dict()
    context_dict = OperationContext.get_instance().get_context_dict()
    exception_queue = mp.Queue()
    # TODO: change to support streaming output
    p = mp.Process(
        target=execute_flow_request_multiprocessing_impl,
        args=(
            execute_flow_func,
            config,
            pid,
            request,
            return_dict,
            exception_queue,
            context_dict,
        ),
    )
    p.start()

    if isinstance(request, BulkRunRequestV2):
        logger.info("Starting to check process %s status for run %s", p.pid, request.flow_run_id)
        start_thread_to_monitor_request_V2_handler_process(
            config=config,
            request=request,
            process=p,
        )
        p.join(timeout=BULKRUN_SUBMISSION_TIMEOUT)

        if p.is_alive():
            logger.error(f"[{p.pid}] Stop bulkrun subprocess for exceeding {BULKRUN_SUBMISSION_TIMEOUT} seconds.")
            p.terminate()
            p.join()
            raise FlowRunTimeoutError(BULKRUN_SUBMISSION_TIMEOUT)
    elif isinstance(request, AsyncFlowRequest) or isinstance(request, AsyncSingleNodeRequest):
        logger.info("Starting to check process %s status for run %s", p.pid, request.flow_run_id)
        start_thread_to_monitor_async_run_status(request=request, process=p)
        p.join(timeout=ASYNC_RUN_SUBMISSION_TIMEOUT)

        if p.is_alive():
            system_logger.warning(f"[{p.pid}] Try to stop async flow subprocess.")
            try:
                os.kill(p.pid, signal.SIGINT)
                p.join()
                logger.error(
                    f"[{p.pid}] Stopped async flow subprocess for exceeding {ASYNC_RUN_SUBMISSION_TIMEOUT} seconds."
                )
                raise FlowRunTimeoutError(ASYNC_RUN_SUBMISSION_TIMEOUT)
            except ProcessLookupError:
                system_logger.warning(f"[{p.pid}] Process not found, it may already terminated.")
                pass
    else:
        # MT timeout 300s for sync submission.
        # Timeout longer than MT to avoid exception thrown early
        p.join(timeout=SYNC_SUBMISSION_TIMEOUT)

        if p.is_alive():
            logger.error(f"[{p.pid}] Stop flow subprocess for exceeding {SYNC_SUBMISSION_TIMEOUT} seconds.")
            p.terminate()
            p.join()
            raise FlowRunTimeoutError(SYNC_SUBMISSION_TIMEOUT)
    logger.info("Process %s finished", p.pid)

    # when p is killed by signal, exitcode will be negative without exception
    if p.exitcode and p.exitcode > 0:
        exception = None
        try:
            exception = exception_queue.get(timeout=WAIT_SUBPROCESS_EXCEPTION_TIMEOUT)
        except Exception:
            pass
        # JsonSerializedPromptflowException will be raised here
        # no need to change to PromptflowException since it will be handled in app.handle_exception
        # we can unify the exception when we decide to expose executor.execute as an public API
        if exception is not None:
            raise exception

    default_result = {}
    # For batch run, result should be a BatchResult object or None.
    if isinstance(request, BulkRunRequestV2):
        default_result = None
    result = return_dict.get("result", default_result)

    logger.info("[%s] Child process finished!", pid)
    return result


def parse_inputs_and_other_nodes_outputs(inputs_from_payload: Dict):
    updated_node_inputs = {}
    other_nodes_outputs = {}
    for k, v in inputs_from_payload.items():
        if FlowInputAssignment.is_flow_input(k):
            updated_k: str = FlowInputAssignment.deserialize(k).value
            # Flow input.
            updated_node_inputs.update({updated_k: v})
        else:
            # Put other node's output in result.
            node_name = SingleNodeRequestV2.get_node_name_from_node_inputs_key(k)
            other_nodes_outputs.update({node_name: v})
    return updated_node_inputs, other_nodes_outputs


def post_process_node_result(result: RunInfo, request: SingleNodeRequestV2):
    if result is None:
        return
    credential_scrubber = CredentialScrubber()
    for c in get_credential_list_for_v2_request(request):
        credential_scrubber.add_str(c)
    logs = result.logs
    if logs is not None:
        logs["stdout"] = credential_scrubber.scrub(logs["stdout"])
        logs["stderr"] = credential_scrubber.scrub(logs["stderr"])
        result.logs = logs


def execute_node_request(config: RuntimeConfig, request: SingleNodeRequestV2):
    origin_wd = os.getcwd()
    working_dir = None
    try:
        if request.flow_source.flow_source_type != FlowSourceType.AzureFileShare:
            raise UnexpectedFlowSourceType(message_format="Node request should be from Azure File Share")
        working_dir = fill_working_dir(
            config.deployment.compute_type,
            request.flow_source.flow_source_info,
            request.flow_run_id,
            request.flow_source.flow_dag_file,
        )
        dag_file = request.flow_source.flow_dag_file

        load_and_apply_env_variables(
            dag_file, working_dir=working_dir, environment_variables_overrides=request.environment_variables
        )

        connection_names = get_used_connection_names_from_environment_variables()
        built_connections = build_connection_dict(
            connection_names=connection_names,
            subscription_id=config.deployment.subscription_id,
            resource_group=config.deployment.resource_group,
            workspace_name=config.deployment.workspace_name,
        )
        update_environment_variables_with_connections(built_connections)

        # Node run doesn't need to set storage.
        node_inputs, other_nodes_outputs = parse_inputs_and_other_nodes_outputs(request.inputs)
        os.chdir(working_dir)
        output_sub_dir = request.output_sub_dir
        if output_sub_dir is None:
            logger.warning(
                "The node request is missing the 'output_sub_dir' field, which is not as expected. Files generated"
                "during execution will be saved to the current flow directory. Please update your client to the latest"
                "version."
            )
            output_sub_dir = "."
        if Path(output_sub_dir).is_absolute():
            raise UnexpectedOutputSubDir(
                message_format="Node test output sub directory '{output_sub_dir}' must be a relative path,"
                "not an absolute path.",
                output_sub_dir=output_sub_dir,
            )
        result = FlowExecutor.load_and_exec_node(
            flow_file=dag_file,
            node_name=request.node_name,
            output_sub_dir=output_sub_dir,
            flow_inputs=node_inputs,
            dependency_nodes_outputs=other_nodes_outputs,
            connections=request.connections,
            working_dir=working_dir,
            raise_ex=False,
        )
        post_process_node_result(result, request)
        from promptflow._internal import serialize

        return {
            "node_runs": [serialize(result)],
        }
    finally:
        os.chdir(origin_wd)
        # post process: clean up and restore working dir
        # note: no need to clean environment variables, because they are only set in child process
        if working_dir and not config.execution.debug:
            # remove working dir if not debug mode
            if (
                config.deployment.compute_type == ComputeType.COMPUTE_INSTANCE
                and request.flow_source is not None
                and request.flow_source.flow_source_type == FlowSourceType.AzureFileShare
            ):
                # Don't remove working dir when it is CI mounting dir
                pass
            else:
                logger.info("Cleanup working dir %s", working_dir)
                shutil.rmtree(working_dir, ignore_errors=True)


def execute_async_node_request(config: RuntimeConfig, request: AsyncSingleNodeRequest) -> RunInfo:
    # TODO: refactor common code with execute_node_request
    origin_wd = os.getcwd()
    working_dir = None
    tmp_node_dir = None
    try:
        if request.flow_source.flow_source_type != FlowSourceType.AzureFileShare:
            raise UnexpectedFlowSourceType(message_format="Node request should be from Azure File Share")
        working_dir = fill_working_dir(
            config.deployment.compute_type,
            request.flow_source.flow_source_info,
            request.flow_run_id,
            request.flow_source.flow_dag_file,
        )
        dag_file = request.flow_source.flow_dag_file

        load_and_apply_env_variables(
            dag_file, working_dir=working_dir, environment_variables_overrides=request.environment_variables
        )

        connection_names = get_used_connection_names_from_environment_variables()
        built_connections = build_connection_dict(
            connection_names=connection_names,
            subscription_id=config.deployment.subscription_id,
            resource_group=config.deployment.resource_group,
            workspace_name=config.deployment.workspace_name,
        )
        update_environment_variables_with_connections(built_connections)

        node_inputs, _ = parse_inputs_and_other_nodes_outputs(request.inputs)
        tmp_node_dir = Path(gettempdir()) / str(uuid.uuid4())
        flow_yaml_path = Path(working_dir) / dag_file
        node_inputs = convert_url_to_path(flow_yaml_path, node_inputs, tmp_node_dir)

        other_nodes_outputs = request.node_output_paths
        os.chdir(working_dir)

        storage = AsyncRunStorage(
            run_id=request.flow_run_id,
            azure_storage_setting=request.azure_storage_setting,
            is_default_variant=request.is_default_variant,
            node_variant_id=request.node_variant_id,
            deployment_config=config.deployment,
            flow_yaml_path=flow_yaml_path,
        )
        # async single node run inputs from dependency nodes is in blob storage,
        # need to download these blobs and resolve possible multimedia data.
        other_nodes_outputs = storage.download_dependency_nodes_outputs(other_nodes_outputs, tmp_node_dir)

        run_info = FlowExecutor.load_and_exec_node(
            flow_file=dag_file,
            node_name=request.node_name,
            storage=storage,
            flow_inputs=node_inputs,
            dependency_nodes_outputs=other_nodes_outputs,
            connections=request.connections,
            working_dir=working_dir,
            raise_ex=False,
        )

        return run_info
    finally:
        os.chdir(origin_wd)
        if tmp_node_dir:
            shutil.rmtree(tmp_node_dir, ignore_errors=True)
        # post process: clean up and restore working dir
        # note: no need to clean environment variables, because they are only set in child process
        if working_dir and not config.execution.debug:
            # remove working dir if not debug mode
            if (
                config.deployment.compute_type == ComputeType.COMPUTE_INSTANCE
                and request.flow_source is not None
                and request.flow_source.flow_source_type == FlowSourceType.AzureFileShare
            ):
                # Don't remove working dir when it is CI mounting dir
                pass
            else:
                logger.info("Cleanup working dir %s", working_dir)
                shutil.rmtree(working_dir, ignore_errors=True)


def execute_flow_request(config: RuntimeConfig, request: FlowRequestV2):
    origin_wd = os.getcwd()
    working_dir = None
    try:
        if request.flow_source.flow_source_type != FlowSourceType.AzureFileShare:
            raise UnexpectedFlowSourceType(message_format="Flow request should be from Azure File Share")
        working_dir = fill_working_dir(
            config.deployment.compute_type,
            request.flow_source.flow_source_info,
            request.flow_run_id,
            request.flow_source.flow_dag_file,
        )
        dag_file = request.flow_source.flow_dag_file

        load_and_apply_env_variables(
            dag_file, working_dir=working_dir, environment_variables_overrides=request.environment_variables
        )

        connection_names = get_used_connection_names_from_environment_variables()
        built_connections = build_connection_dict(
            connection_names=connection_names,
            subscription_id=config.deployment.subscription_id,
            resource_group=config.deployment.resource_group,
            workspace_name=config.deployment.workspace_name,
        )
        update_environment_variables_with_connections(built_connections)

        # Flow run doesn't need to set storage.
        os.chdir(working_dir)
        flow_id, run_id = request.flow_id, request.flow_run_id
        output_sub_dir = request.output_sub_dir
        if output_sub_dir is None:
            logger.warning(
                "The flow request is missing the 'output_sub_dir' field, which is not as expected. Files generated"
                "during execution will be saved to the current flow directory. Please update your client to the latest"
                "version."
            )
            output_sub_dir = "."
        if Path(output_sub_dir).is_absolute():
            raise UnexpectedOutputSubDir(
                message_format="Flow test output sub directory '{output_sub_dir}' must be a relative path,"
                "not an absolute path.",
                output_sub_dir=output_sub_dir,
            )
        storage = DefaultRunStorage(base_dir=working_dir, sub_dir=Path(output_sub_dir))
        flow_executor = FlowExecutor.create(
            dag_file, request.connections, Path(working_dir), storage=storage, raise_ex=False
        )
        run_tracker = flow_executor._run_tracker
        run_tracker._activate_in_context()
        run_info = run_tracker.start_flow_run(flow_id, run_id, run_id)
        try:
            line_result = flow_executor.exec_line(inputs=request.inputs, index=0, run_id=run_id)
            # TODO: Refine the logic here, avoid returning runs from run_tracker,
            # We should better return the result from line_result and aggregation result.
            flow_executor._add_line_results([line_result])
            if flow_executor.has_aggregation_node:
                inputs_list = {k: [v] for k, v in request.inputs.items()}
                aggregation_inputs_list = {k: [v] for k, v in line_result.aggregation_inputs.items()}
                aggregate_result = flow_executor.exec_aggregation(inputs_list, aggregation_inputs_list, run_id=run_id)
                run_info.metrics = aggregate_result.metrics
            run_tracker.end_run(run_id, result=[])
        except Exception as e:  # We init flow executor with raise_ex=False, so usually, there is no exception.
            logger.exception(f"Run {run_id} failed. Exception: {{customer_content}}", extra={"customer_content": e})
            run_tracker.end_run(run_id, ex=e)
        finally:
            run_tracker._deactivate_in_context()
        return run_tracker.collect_all_run_infos_as_dicts()
    finally:
        os.chdir(origin_wd)
        # post process: clean up and restore working dir
        # note: no need to clean environment variables, because they are only set in child process
        if working_dir and not config.execution.debug:
            # remove working dir if not debug mode
            if (
                config.deployment.compute_type == ComputeType.COMPUTE_INSTANCE
                and request.flow_source is not None
                and request.flow_source.flow_source_type == FlowSourceType.AzureFileShare
            ):
                # Don't remove working dir when it is CI mounting dir
                pass
            else:
                logger.info("Cleanup working dir %s", working_dir)
                shutil.rmtree(working_dir, ignore_errors=True)


def _prepare_flow_inputs_with_reference(request: AsyncFlowRequest, config: RuntimeConfig):
    """
    Prepare flow inputs with reference.

    This function prepares the flow inputs by resolving any references to external files.
    It takes an AsyncFlowRequest object and a RuntimeConfig object as input.

    Example:

    Payload:
    {
        "data_inputs": {
            "main.output": {"universal_link": "https://example.com/input1.json"},
            "main.input": {"inputs": {"key1": "maininputkey1", "key2": "maininputkey2"}},
        },
        "inputs": {"param1": "${main.output.key1}", "param2": "${main.input.key2}", "param3": "static value"},
    }
    Resolved inputs:
    {
        "param1": "mainoutputkey1",
        "param2": "maininputkey2",
        "param3": "static value"
    }

    """
    referenced_inputs = {}
    for key, value in request.data_inputs.items():
        # Should points to a file if universal link is provided.
        if value.universal_link:
            # Avoid using working dir from file share, which will introduce unncessary data transfer.
            working_dir_in_local_folder = get_working_dir_from_run_id(request.flow_run_id)
            target_file = prepare_data(
                value.universal_link,
                destination=working_dir_in_local_folder / "reference" / key,
                runtime_config=config,
            )
            target_file = Path(target_file)
            # target_path from prepare_data could be a file or a dir, even the link points to a file.
            # Runtime will fix prepare_data's behavior in the future.
            if target_file.is_dir():
                logger.info(
                    "Downloaded universal link points to a directory, try to find the file name by splitting link."
                )
                file_name = _get_last_part_of_uri(value.universal_link)
                target_file = target_file / file_name
            # Upstream should only pass in file's universal link.
            if not target_file.is_file():
                raise InvalidDataInputs(
                    message_format=(
                        "The universal link '{link}' for async flow data inputs '{key}' is invalid, "
                        "please guarantee it's a link points to file."
                    ),
                    key=key,
                    link=value.universal_link,
                )
            referenced_inputs[key] = json.loads(target_file.read_text("utf-8"))
            target_file.unlink(missing_ok=True)
        else:
            referenced_inputs[key] = value.inputs
    # Normal inputs in request.inputs could be treated as static value for mapping.
    return apply_inputs_mapping(inputs=referenced_inputs, inputs_mapping=request.inputs)


def execute_async_flow_request(config: RuntimeConfig, request: AsyncFlowRequest) -> FlowRunInfo:
    # TODO: refactor common code with execute_flow_request
    origin_wd = os.getcwd()
    working_dir = None
    tmp_node_outputs_dir = None
    try:
        if request.flow_source.flow_source_type == FlowSourceType.AzureFileShare:
            working_dir = fill_working_dir(
                config.deployment.compute_type,
                request.flow_source.flow_source_info,
                request.flow_run_id,
                request.flow_source.flow_dag_file,
            )
        elif request.flow_source.flow_source_type == FlowSourceType.Snapshot:
            working_dir = get_working_dir_from_run_id(request.flow_run_id)
            download_snapshot(working_dir, config, request)
        else:
            raise UnexpectedFlowSourceType(message_format="Flow request should be from Azure File Share or Snapshot")

        dag_file = request.flow_source.flow_dag_file

        # For now, we only need do mapping for snapshot's evaluation run.
        # But check flow source type to determine whether to do mapping seems not a good idea.
        # Just add mapping for all async flow request for now.
        inputs = _prepare_flow_inputs_with_reference(request, config=config)

        load_and_apply_env_variables(
            dag_file, working_dir=working_dir, environment_variables_overrides=request.environment_variables
        )

        connection_names = get_used_connection_names_from_environment_variables()
        built_connections = build_connection_dict(
            connection_names=connection_names,
            subscription_id=config.deployment.subscription_id,
            resource_group=config.deployment.resource_group,
            workspace_name=config.deployment.workspace_name,
        )
        update_environment_variables_with_connections(built_connections)

        os.chdir(working_dir)
        run_id = request.flow_run_id
        flow_yaml_path = Path(working_dir) / dag_file
        storage = AsyncRunStorage(
            run_id=run_id,
            azure_storage_setting=request.azure_storage_setting,
            deployment_config=config.deployment,
            flow_yaml_path=flow_yaml_path,
        )
        flow_executor = FlowExecutor.create(
            dag_file, request.connections, Path(working_dir), storage=storage, raise_ex=False
        )
        tmp_node_outputs_dir = Path(gettempdir()) / str(uuid.uuid4())
        inputs = convert_url_to_path(flow_yaml_path, inputs, tmp_node_outputs_dir)
        line_result = flow_executor.exec_line(inputs=inputs, index=0, run_id=run_id)
        flow_executor._add_line_results([line_result])
        if flow_executor.has_aggregation_node:
            inputs_list = {k: [v] for k, v in inputs.items()}
            aggregation_inputs_list = {k: [v] for k, v in line_result.aggregation_inputs.items()}
            aggregate_result = flow_executor.exec_aggregation(inputs_list, aggregation_inputs_list, run_id=run_id)
            # update aggregation metrics in flow run info
            storage.update_aggregation_metrics(aggregate_result.metrics)
        if line_result:
            return line_result.run_info
        return None
    finally:
        os.chdir(origin_wd)
        if tmp_node_outputs_dir:
            shutil.rmtree(tmp_node_outputs_dir, ignore_errors=True)
        # post process: clean up and restore working dir
        # note: no need to clean environment variables, because they are only set in child process
        # TODO: need to remove the debug flag check
        if working_dir and not config.execution.debug:
            # remove working dir if not debug mode
            if (
                config.deployment.compute_type == ComputeType.COMPUTE_INSTANCE
                and request.flow_source is not None
                and request.flow_source.flow_source_type == FlowSourceType.AzureFileShare
            ):
                # Don't remove working dir when it is CI mounting dir
                pass
            else:
                logger.info("Cleanup working dir %s", working_dir)
                shutil.rmtree(working_dir, ignore_errors=True)


def get_working_dir_from_run_id(run_id: str):
    container_path = Path(f"requests/{run_id}").resolve()
    return Path(HOST_MOUNT_PATH) / str(container_path)[1:]


def execute_csharp_bulk_run_request(config: RuntimeConfig, request: BulkRunRequestV2, working_dir: Path):
    working_dir = get_working_dir_from_run_id(request.flow_run_id)
    try:
        output_dir = working_dir / ".flow_outputs"
        run_storage: AzureMLRunStorageV2 = config.get_run_storage(
            workspace_access_token=None,
            azure_storage_setting=request.azure_storage_setting,
            run_mode=request.get_run_mode(),
            output_dir=output_dir,
        )
        run_history_client = config.get_run_history_client()
        mlflow_tracking_uri = config.set_mlflow_tracking_uri()
        mlflow_helper = MlflowHelper(mlflow_tracking_uri=mlflow_tracking_uri)
        batch_result = None
        output_dir.mkdir(exist_ok=True)
        input_dicts = _prepare_input_data(config, request, working_dir)
        dag_file = request.flow_source.flow_dag_file
        # TODO: Set batch_timeout_sec after csharp batch engine supports timeout.
        batch_engine = BatchEngine(
            flow_file=dag_file,
            working_dir=working_dir,
            storage=run_storage,
            # Use run id in container name to avoid name conflict.
            container_name=f"executor-{request.flow_run_id}",
            log_path=request.log_path,
            worker_count=request.worker_count,
        )
        # Start a thread to monitor csharp batch run status to handle cancel case.
        start_thread_to_monitor_csharp_batch_run(run_history_client, request, batch_engine)
        try:
            mlflow_helper.start_run(run_id=request.flow_run_id, create_if_not_exist=True)
            logger.info("Running batch engine...")
            # TODO: Set resume_from_run_storage and resume_from_run_output_dir if need to support csharp resume.
            batch_result: BatchResult = batch_engine.run(
                input_dirs=input_dicts,
                inputs_mapping=request.inputs_mapping,
                output_dir=output_dir,
                run_id=request.flow_run_id,
                max_lines_count=MAX_ROWS_COUNT,
            )
        except Exception as ex:
            # Mark the run as failed and do not raise exception.
            logger.exception("Batch run failed. Exception: {customer_content}", extra={"customer_content": ex})
            error_reponse_dict = ErrorResponse.from_exception(ex).to_dict()
            mlflow_helper.end_aml_root_run(request.flow_run_id, Status.Failed.value, error_reponse_dict)
            return batch_result

        logger.info("Post processing batch result...")
        post_process_root_run(request.flow_run_id, batch_result, mlflow_helper, run_history_client, run_storage)
        return batch_result
    except FileNotFoundError as e:
        raise FlowFileNotFound("Cannot find flow file. Error message={e.message}") from e
    except ClientAuthenticationError as e:
        raise InvalidClientAuthentication(message="Cannot get client authentication") from e
    except Exception as e:
        logger.error("Failed to execute bulk run request. Exception: {customer_content}", extra={"customer_content": e})
        raise


def post_process_root_run(
    run_id: str,
    batch_result: BatchResult,
    mlflow_helper: MlflowHelper,
    run_history_client: RunHistoryClient,
    run_storage: AzureMLRunStorageV2,
    log_patterns: List[str] = None,
):
    if batch_result is None:
        return

    # Write status summary.
    status_summary = {f"__pf__.nodes.{k}": v for k, v in batch_result.node_status.items()}
    status_summary.update(
        {
            "__pf__.lines.completed": batch_result.completed_lines,
            "__pf__.lines.failed": batch_result.failed_lines,
        }
    )
    mlflow_helper.persist_status_summary(status_summary, run_id)

    # Upload metrics
    mlflow_helper.upload_metrics_to_run_history(run_id, batch_result.metrics)

    # Update properties.
    properties = mlflow_helper.generate_properties(batch_result.system_metrics.to_dict())
    mlflow_helper.update_run_history_properties(properties)

    # Register artifacts.
    output_asset_infos = run_storage.register_root_run_artifacts(run_id, batch_result.status)
    if output_asset_infos is not None:
        run_history_client.patch_run(run_id, output_asset_infos)

    # End run.
    error_reponse_dict = _get_error_response_dict(batch_result, mlflow_helper, log_patterns)
    mlflow_helper.end_aml_root_run(run_id, batch_result.status.value, error_reponse_dict)


def _get_error_response_dict(batch_result: BatchResult, mlflow_helper: MlflowHelper, log_patterns: List[str] = None):
    if batch_result.error_summary:
        error_dict = None

        # We should first check batch run level error, and then check each line error.
        if hasattr(batch_result.error_summary, "batch_error_dict") and batch_result.error_summary.batch_error_dict:
            error_dict = batch_result.error_summary.batch_error_dict
        elif batch_result.error_summary.error_list:
            error_list = [e.error for e in batch_result.error_summary.error_list]
            error_dict = generate_error_dict_for_root_run(error_list, batch_result.total_lines)
        elif getattr(batch_result.error_summary, "aggr_error_dict", None):
            # If no error in child runs, but error in aggregation node runs, use the first error as root run's error.
            # Use getattr to avoid error
            # when batch_result.error_summary does not have "aggr_error_dict" attribute (for promptflow<1.3.0).
            # TODO: Remove getattr after promptflow<1.3.0 is not used in cloud anymore.
            error_dict = next(iter(batch_result.error_summary.aggr_error_dict.values()))

        if error_dict:
            mlflow_helper.overwrite_cloud_batch_error_message(error_dict)
            if log_patterns:
                return mlflow_helper.get_safe_tool_execution_error_response(error_dict)
            return ErrorResponse.from_error_dict(error_dict).to_dict()

    return None


def _prepare_input_data(config: RuntimeConfig, request: BulkRunRequestV2, working_dir: Path) -> Dict:
    input_dicts = {}
    for input_key, input_url in request.data_inputs.items():
        with ProgressTimer(logger, "Resolve data from url"):
            # resolve data uri to local data
            local_path = prepare_data(input_url, destination=working_dir / "inputs" / input_key, runtime_config=config)
            input_dicts[input_key] = local_path
    return input_dicts


def _prepare_resume_data(
    resume_from_run_id: str, run_history_client: RunHistoryClient, config: RuntimeConfig, working_dir: Path
):
    resume_from_run_details = run_history_client.get_run_details(resume_from_run_id)
    resume_from_run_outputs = resume_from_run_details.get("outputs")
    if resume_from_run_outputs is None:
        system_logger.warning(f"Get no resume run {resume_from_run_id} outputs asset info, return None.")
        return None, None

    resume_data_dir = working_dir / "resume_data"
    resume_flow_outputs_dir = None
    resume_debug_info_dir = None
    resume_from_run_storage = None

    resume_flow_outputs = resume_from_run_outputs.get("flow_outputs")
    if resume_flow_outputs is not None:
        resume_flow_outputs_asset_uri = _convert_asset_id_to_asset_uri(resume_flow_outputs.get("assetId"))
        resume_flow_outputs_dir = resume_data_dir / "flow_outputs"
        prepare_data(
            uri=resume_flow_outputs_asset_uri,
            destination=resume_flow_outputs_dir,
            runtime_config=config,
        )
        system_logger.info(f"Downloaded resume run {resume_from_run_id} flow output asset.")
    else:
        system_logger.warning(f"Get no resume run {resume_from_run_id} flow outputs.")

    resume_debug_info = resume_from_run_outputs.get("debug_info")
    if resume_debug_info is not None:
        resume_debug_info_asset_uri = _convert_asset_id_to_asset_uri(resume_debug_info.get("assetId"))
        resume_debug_info_dir = resume_data_dir / "debug_info"
        prepare_data(
            uri=resume_debug_info_asset_uri,
            destination=resume_debug_info_dir,
            runtime_config=config,
        )
        # import package here for backward compatibility
        from promptflow.runtime.storage.resume_from_run_storage import ResumeFromRunStorage

        resume_from_run_storage = ResumeFromRunStorage(resume_debug_info_dir)
        system_logger.info(f"Downloaded resume run {resume_from_run_id} debug info asset.")
    else:
        system_logger.info(f"Get no resume run {resume_from_run_id} debug info.")

    return resume_flow_outputs_dir, resume_from_run_storage


def _convert_asset_id_to_asset_uri(asset_id: str):
    asset_id_regex = "azureml://locations/([^/]+)/workspaces/([^/]+)/data/([^/]+)/versions/(.+)"
    if re.match(asset_id_regex, asset_id):
        _, _, asset_name, version = re.match(asset_id_regex, asset_id).groups()
        asset_uri_format = "azureml:{asset_name}:{version}"
        asset_uri = asset_uri_format.format(asset_name=asset_name, version=version)
        return asset_uri
    else:
        raise InvalidAssetId(message_format="Invalid asset id: {asset_id}", asset_id=asset_id)


def download_snapshot(working_dir: Union[str, Path], config: RuntimeConfig, request: SubmissionRequestBaseV2):
    if request.flow_source.flow_source_type != FlowSourceType.Snapshot:
        raise UnexpectedFlowSourceType(message_format="Bulk run request data should be from Snapshot.")
    logger.info(f"Downloading snapshot to {working_dir}")
    if isinstance(working_dir, str):
        working_dir = Path(working_dir)

    working_dir.mkdir(parents=True, exist_ok=True)
    snapshot_client = config.get_snapshot_client()
    snapshot_client.download_snapshot(request.flow_source.flow_source_info.snapshot_id, working_dir)
    logger.info(f"Successfully download snapshot to {working_dir}")


def execute_bulk_run_request(config: RuntimeConfig, request: BulkRunRequestV2):
    origin_wd = os.getcwd()
    working_dir = None
    try:
        working_dir = get_working_dir_from_run_id(request.flow_run_id)
        dag_file = request.flow_source.flow_dag_file
        load_and_apply_env_variables(
            dag_file, working_dir=working_dir, environment_variables_overrides=request.environment_variables
        )

        connection_names = get_used_connection_names_from_environment_variables()
        built_connections = build_connection_dict(
            connection_names=connection_names,
            subscription_id=config.deployment.subscription_id,
            resource_group=config.deployment.resource_group,
            workspace_name=config.deployment.workspace_name,
        )
        update_environment_variables_with_connections(built_connections)

        run_id = request.flow_run_id
        output_dir = working_dir / ".flow_outputs"
        run_storage = config.get_run_storage(
            workspace_access_token=None,
            azure_storage_setting=request.azure_storage_setting,
            run_mode=request.get_run_mode(),
            output_dir=output_dir,
        )
        run_history_client = config.get_run_history_client()
        mlflow_tracking_uri = config.set_mlflow_tracking_uri()
        mlflow_helper = MlflowHelper(mlflow_tracking_uri=mlflow_tracking_uri)
        batch_result = None

        try:
            output_dir.mkdir(exist_ok=True)
            # For bulk run, PFS should always assign data_inputs, otherwise it is one system error.
            if not request.data_inputs:
                raise DataInputsNotfound(message_format="Data inputs not found in bulk run request.")
            # Start to download inputs.
            input_dicts = _prepare_input_data(config, request, working_dir)
            os.chdir(working_dir)

            batch_engine = BatchEngine(
                flow_file=dag_file,
                working_dir=working_dir,
                connections=request.connections,
                storage=run_storage,
                batch_timeout_sec=request.batch_timeout_sec,
                worker_count=request.worker_count,
            )

            mlflow_helper.start_run(run_id=request.flow_run_id, create_if_not_exist=True)

            # If have resume run, runtime should download resume run's flow output and debug info firstly.
            # Check if ResumeBatchRun feature exist to avoid error when runtime call a older version promptflow package.
            if request.resume_from_run_id is not None and check_executor_feature_exist("ResumeBatchRun"):
                logger.info(f"Prepare resume data for run {run_id}, resume from run {request.resume_from_run_id}.")
                resume_flow_outputs_dir, resume_from_run_storage = _prepare_resume_data(
                    request.resume_from_run_id, run_history_client, config, working_dir
                )
                batch_result: BatchResult = batch_engine.run(
                    input_dirs=input_dicts,
                    inputs_mapping=request.inputs_mapping,
                    output_dir=output_dir,
                    run_id=run_id,
                    max_lines_count=None if request.batch_timeout_sec else MAX_ROWS_COUNT,
                    resume_from_run_storage=resume_from_run_storage,
                    resume_from_run_output_dir=resume_flow_outputs_dir,
                )
            else:
                if request.resume_from_run_id is not None:
                    logger.warning(
                        "Batch run resume is not supported in current promptflow version, "
                        "the batch run will be re-executed. Please upgrade promptflow package to use resume feature."
                    )
                batch_result: BatchResult = batch_engine.run(
                    input_dirs=input_dicts,
                    inputs_mapping=request.inputs_mapping,
                    output_dir=output_dir,
                    run_id=run_id,
                    max_lines_count=None if request.batch_timeout_sec else MAX_ROWS_COUNT,
                )

            logger.info("Post processing batch result...")
            post_process_root_run(
                run_id,
                batch_result,
                mlflow_helper,
                run_history_client,
                run_storage,
                request.get_log_filter_patterns(),
            )
            return batch_result
        except FileNotFoundError as e:
            raise FlowFileNotFound("Cannot find flow file. Error message={e.message}") from e
        except Exception as e:
            logger.exception("Batch run failed. Exception: {customer_content}", extra={"customer_content": e})
            error_reponse_dict = ErrorResponse.from_exception(e).to_dict()
            mlflow_helper.end_aml_root_run(request.flow_run_id, Status.Failed.value, error_reponse_dict)
            return batch_result
        finally:
            os.chdir(origin_wd)
    except ClientAuthenticationError as e:
        raise InvalidClientAuthentication(message="Cannot get client authentication") from e


def get_credential_list_for_v2_request(req: SubmissionRequestBaseV2) -> List[str]:
    credential_list = ConnectionManager(req.connections).get_secret_list()
    if req.app_insights_instrumentation_key:
        credential_list.append(req.app_insights_instrumentation_key)
    return credential_list


def get_log_context_from_v2_request(request: SubmissionRequestBaseV2) -> SystemLogContext:
    # Add root_flow_run_id and run_mode into logger's custom dimensions.
    run_mode = request.get_run_mode()
    custom_dimensions = {
        "root_flow_run_id": request.flow_run_id,
        "run_mode": run_mode.name if run_mode is not None else "",
    }
    edition = OperationContext.get_instance().get("edition", PromptflowEdition.COMMUNITY)
    file_type = FileType.Blob if edition == PromptflowEdition.ENTERPRISE else FileType.Local
    return SystemLogContext(
        file_path=request.log_path,
        run_mode=run_mode,
        credential_list=get_credential_list_for_v2_request(request),
        file_type=file_type,
        custom_dimensions=custom_dimensions,
        app_insights_instrumentation_key=request.app_insights_instrumentation_key,
        log_filtering_patterns=request.get_log_filter_patterns(),
        input_logger=logger,
    )


def get_log_context_for_cancel_request(request: CancelRunRequest) -> SystemLogContext:
    custom_dimensions = {
        "root_flow_run_id": request.flow_run_id,
    }
    edition = OperationContext.get_instance().get("edition", PromptflowEdition.COMMUNITY)
    file_type = FileType.Blob if edition == PromptflowEdition.ENTERPRISE else FileType.Local
    return SystemLogContext(
        file_path=request.log_path,
        file_type=file_type,
        custom_dimensions=custom_dimensions,
        app_insights_instrumentation_key=request.app_insights_instrumentation_key,
        credential_list=[request.app_insights_instrumentation_key] if request.app_insights_instrumentation_key else [],
        input_logger=logger,
    )


def start_thread_to_monitor_request_V2_handler_process(
    config: RuntimeConfig, request: SubmissionRequestBaseV2, process
):
    """Start a thread to monitor V2 request handler process.
    When request cancel is received, it will
    1. terminate the request handler process.
    2. mark the run as canceled.
    """

    def terminate_process():
        if process.is_alive():
            children = psutil.Process(process.pid).children(recursive=True)
            for child in children:
                try:
                    child.terminate()
                    system_logger.info("Successfully terminated child process with pid %s", child.pid)
                except NoSuchProcess:
                    system_logger.info("Child process %s already terminated and not found, skipping", child.pid)
                    pass
            process.terminate()
            system_logger.info("Successfully terminated process with pid %s", process.pid)
        else:
            system_logger.info("Process already terminated")
        return True

    # add timeout & retry to avoid request stuck issue
    @retry(TimeoutError, tries=3)
    @timeout(timeout_seconds=MONITOR_REQUEST_TIMEOUT)
    def get_runhistory_client_from_config_with_retry() -> RunHistoryClient:
        return config.get_run_history_client()

    @retry(TimeoutError, tries=10)
    @timeout(timeout_seconds=MONITOR_REQUEST_TIMEOUT)
    def cancel_run_with_retry(runhistory_client: RunHistoryClient, run_id):
        return runhistory_client.update_run_status(run_id=run_id, run_status=Status.Canceled)

    def monitor_run_status(run_id: str, terminate_process, context: contextvars.Context):
        try:
            runhistory_client = get_runhistory_client_from_config_with_retry()
            set_context(context)
            logger.info("Start checking run status for run %s", run_id)
            while True:
                # keep monitoring to make sure long running process can be terminated
                time.sleep(STATUS_CHECKER_INTERVAL)

                run_status = get_run_status_with_retry(runhistory_client=runhistory_client, run_id=run_id)
                if run_status is None:
                    logger.info("Run %s not found, end execution monitoring", run_id)
                    return
                system_logger.info("Run %s is in progress, Execution status: %s", run_id, run_status)
                if run_status in [Status.Canceled.value, Status.CancelRequested.value]:
                    logger.info("Cancel requested for run %s", run_id)
                    try:
                        # terminate the process gracefully
                        terminated = terminate_process()
                        if not terminated:
                            continue
                        logger.info("Updating status for run %s", run_id)
                        cancel_run_with_retry(runhistory_client=runhistory_client, run_id=run_id)
                        logger.info("Successfully canceled run %s", run_id)
                        # mark the run as canceled
                        return
                    except Exception as e:
                        logger.error("Failed to kill process for run %s due to %s", run_id, e, exc_info=True)
                        return
                elif Status.is_terminated(run_status):
                    logger.debug("Run %s is in terminate status %s", run_id, run_status)
                    return
        except Exception as e:
            system_logger.warning("Failed to monitor run status for run %s due to %s", run_id, e, exc_info=True)

    run_id = request.flow_run_id
    # cancel the parent run(run_id) as well as all its child runs
    thread = threading.Thread(
        name="monitor_bulk_run_status",
        target=monitor_run_status,
        kwargs={
            "run_id": run_id,
            "terminate_process": terminate_process,
            "context": contextvars.copy_context(),
        },
        daemon=True,
    )
    thread.start()


def start_thread_to_monitor_async_run_status(request: Union[AsyncFlowRequest, AsyncSingleNodeRequest], process):
    """Start a thread to monitor async run status.
    When the run is cancelling, the status will be updated to CancelRequested.
    We need to kill executor process with SIGINT signal.
    """

    def kill_process():
        if process.is_alive():
            try:
                # Executor will handle SIGINT.
                os.kill(process.pid, signal.SIGINT)
                system_logger.info(f"Kill process {process.pid} with SIGINT")
                # wait for 40s for executor process to gracefully shutdown
                process.join(timeout=40)
                if process.is_alive():
                    # force kill if still alive
                    os.kill(process.pid, signal.SIGKILL)
                    system_logger.info(f"Kill process {process.pid} with SIGKILL")
                system_logger.info(f"Successfully terminated process {process.pid}")
            except ProcessLookupError:
                system_logger.info(f"Process {process.pid} not found, it may already terminated.")
                pass
        else:
            system_logger.info("Process already terminated")
        return True

    def monitor_async_run_status(request: Union[AsyncFlowRequest, AsyncSingleNodeRequest], kill_process):
        run_id = request.flow_run_id
        try:
            is_single_node_run = isinstance(request, AsyncSingleNodeRequest)
            if is_single_node_run:
                storage = AsyncRunStorage(
                    run_id=run_id,
                    azure_storage_setting=request.azure_storage_setting,
                    is_default_variant=request.is_default_variant,
                    node_variant_id=request.node_variant_id,
                )
            else:
                storage = AsyncRunStorage(
                    run_id=run_id,
                    azure_storage_setting=request.azure_storage_setting,
                )
            system_logger.info(f"Start checking async run status for run {run_id}")
            while True:
                time.sleep(ASYNC_RUN_STATUS_CHECKER_INTERVAL)

                if is_single_node_run:
                    run_status = storage.get_node_run_status(request.node_name)
                else:
                    run_status = storage.get_flow_run_status()
                if run_status is None:
                    system_logger.info(f"Can not find status of async run {run_id}, stop monitoring.")
                    return

                if run_status == Status.CancelRequested.value:
                    system_logger.info(f"Cancel requested for async run {run_id}")
                    try:
                        terminated = kill_process()
                        if not terminated:
                            continue
                        # set the run to Canceled status in runtime if executor not updated successfully
                        if is_single_node_run:
                            status = storage.get_node_run_status(request.node_name)
                            if status != Status.Canceled.value:
                                storage.cancel_node_run(request.node_name)
                        else:
                            status = storage.get_flow_run_status()
                            if status != Status.Canceled.value:
                                storage.cancel_flow_run()
                        system_logger.info(f"Successfully canceled async run {run_id}")
                        return
                    except Exception as e:
                        system_logger.error(f"Failed to kill process for run {run_id} due to {e}", exc_info=True)
                        return
                elif Status.is_terminated(run_status):
                    system_logger.info(f"Async run {run_id} is in terminate status {run_status}")
                    return
        except Exception as e:
            system_logger.warning(f"Failed to monitor run status for run {run_id} due to {e}", exc_info=True)

    thread = threading.Thread(
        name="monitor_async_run_status",
        target=monitor_async_run_status,
        kwargs={
            "request": request,
            "kill_process": kill_process,
        },
        daemon=True,
    )
    thread.start()


def start_thread_to_monitor_csharp_batch_run(
    run_history_client: RunHistoryClient, request: SubmissionRequestBaseV2, batch_engine: BatchEngine
):
    """Start a thread to monitor csharp batch run status.
    When request cancel is received, it will call batch_engine.cancel() method to kill executor container.
    """

    def monitor_csharp_batch_run_status(run_id: str, context: contextvars.Context):
        try:
            set_context(context)
            logger.info("Start checking run status for run %s", run_id)
            while True:
                time.sleep(STATUS_CHECKER_INTERVAL)
                run_status = get_run_status_with_retry(runhistory_client=run_history_client, run_id=run_id)
                if run_status is None:
                    logger.info("Run %s not found, end execution monitoring", run_id)
                    return
                system_logger.info("Run %s is in progress, Execution status: %s", run_id, run_status)
                if run_status in [Status.Canceled.value, Status.CancelRequested.value]:
                    logger.info("Cancel requested for run %s", run_id)
                    try:
                        batch_engine.cancel()
                        logger.info("Successfully canceled run %s in batch engine", run_id)
                        return
                    except Exception as e:
                        logger.error("Failed to cancel run %s in batch engine due to %s", run_id, e, exc_info=True)
                        return
                elif Status.is_terminated(run_status):
                    logger.debug("Run %s is in terminate status %s", run_id, run_status)
                    return
        except Exception as e:
            system_logger.warning("Failed to monitor run status for run %s due to %s", run_id, e, exc_info=True)

    run_id = request.flow_run_id
    thread = threading.Thread(
        name="monitor_csharp_batch_run_status",
        target=monitor_csharp_batch_run_status,
        kwargs={
            "run_id": run_id,
            "context": contextvars.copy_context(),
        },
        daemon=True,
    )
    thread.start()


@contextmanager
def reset_and_close_logger():
    """
    In child process, reset telemetry handler,
    because the previous thread in parent process won't work in this process.
    After, close handler otherwise logs will be lost.
    """
    reset_telemetry_log_handler(logger)
    try:
        yield
    finally:
        close_telemetry_log_handler(logger)


@retry(TimeoutError, tries=3)
@timeout(timeout_seconds=MONITOR_REQUEST_TIMEOUT)
def get_run_status_with_retry(runhistory_client: RunHistoryClient, run_id: str):
    run_info = runhistory_client.get_run(run_id=run_id)
    return run_info.get("status", "")


def check_executor_feature_exist(feature_name: str):
    executor_feature_name_list = [feature.name for feature in get_feature_list()]
    return feature_name in executor_feature_name_list
