# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import multiprocessing
import os
import shutil
import signal
import sys
import uuid
from contextvars import ContextVar
from datetime import datetime
from pathlib import Path
from typing import Dict

from flask import Flask, Response, g, jsonify, request

from promptflow._internal import (
    VERSION,
    ErrorResponse,
    ExceptionPresenter,
    JsonSerializedPromptflowException,
    OperationContext,
    _change_working_dir,
    collect_package_tools,
    generate_prompt_meta,
    generate_python_meta,
    generate_tool_meta_dict_by_file,
    inject_sys_path,
)
from promptflow.batch._result import BatchResult
from promptflow.contracts.run_info import FlowRunInfo, RunInfo
from promptflow.contracts.run_mode import RunMode
from promptflow.contracts.tool import ToolType
from promptflow.runtime._errors import OpenURLNotFoundError
from promptflow.runtime.capability import get_runtime_api_list, get_total_feature_list
from promptflow.runtime.connections import build_connection_dict
from promptflow.runtime.constants import SYNC_REQUEST_TIMEOUT_THRESHOLD
from promptflow.runtime.contracts._errors import InvalidFlowSourceType
from promptflow.runtime.contracts.azure_storage_setting import AzureStorageSetting
from promptflow.runtime.contracts.runtime import (
    AsyncFlowRequest,
    AsyncSingleNodeRequest,
    BulkRunRequestV2,
    CancelRunRequest,
    FlowRequestV2,
    FlowSourceType,
    MetaV2Request,
    SingleNodeRequestV2,
)
from promptflow.runtime.data import prepare_blob_directory
from promptflow.runtime.storage.async_run_storage import AsyncRunStorage
from promptflow.runtime.utils._debug_log_helper import generate_safe_error_stacktrace
from promptflow.runtime.utils._flow_dag_parser import get_language
from promptflow.runtime.utils._run_status_helper import mark_run_as_preparing_in_runhistory
from promptflow.runtime.utils.internal_logger_utils import (
    TelemetryLogHandler,
    set_app_insights_instrumentation_key,
    set_custom_dimensions_to_logger,
    system_logger,
)
from promptflow.runtime.utils.run_result_parser import RunResultParser

from ._errors import (
    AzureStorageSettingMissing,
    GenerateMetaTimeout,
    NodeVariantInfoInvalid,
    NoToolTypeDefined,
    RuntimeTerminatedByUser,
)
from .runtime import (
    PromptFlowRuntime,
    download_snapshot,
    execute_async_flow_request,
    execute_async_node_request,
    execute_bulk_run_request,
    execute_csharp_bulk_run_request,
    execute_flow_request,
    execute_node_request,
    get_log_context_for_cancel_request,
    get_log_context_from_v2_request,
    get_working_dir_from_run_id,
    reset_and_close_logger,
)
from .runtime_config import load_runtime_config
from .utils import log_runtime_pf_version, logger, multi_processing_exception_wrapper, setup_contextvar
from .utils._contract_util import to_snake_case
from .utils._flow_source_helper import fill_working_dir

app = Flask(__name__)

collect_package_tools()  # Collect package tools when runtime starts to avoid loading latency in each request.

active_run_context = ContextVar("active_run_context", default=None)


def signal_handler(signum, frame):
    signame = signal.Signals(signum).name
    logger.info("Runtime stopping. Handling signal %s (%s)", signame, signum)
    try:
        active_run = active_run_context.get()
        if active_run is not None:
            ex = RuntimeTerminatedByUser(
                f"Flow run failed because runtime is terminated at {datetime.utcnow().isoformat()}. "
                f"It may be caused by runtime version update or compute instance stop."
            )
            if isinstance(active_run, BulkRunRequestV2):
                logger.info("Update bulk run to failed on exit. run id: %s", active_run.flow_run_id)
                runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
                runtime.mark_flow_runs_v2_as_failed(active_run, {"flow_run_id": active_run.flow_run_id}, ex)
            elif isinstance(active_run, AsyncFlowRequest):
                logger.info("Update async flow run to failed on exit. run id: %s", active_run.flow_run_id)
                _mark_async_run_as_failed(ex, active_run.flow_run_id, active_run.azure_storage_setting)
            elif isinstance(active_run, AsyncSingleNodeRequest):
                logger.info("Update async single node run to failed on exit. run id: %s", active_run.flow_run_id)
                _mark_async_run_as_failed(
                    ex,
                    active_run.flow_run_id,
                    active_run.azure_storage_setting,
                    active_run.node_name,
                    active_run.is_default_variant,
                    active_run.node_variant_id,
                )
    except Exception:
        logger.warning("Error when handling runtime stop signal", exc_info=True)
    finally:
        sys.exit(1)


def register_signal_handler():
    # register signal handler to gracefully shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)


@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors with correct error code & error category."""

    resp = generate_error_response(e)

    return jsonify(resp.to_dict()), resp.response_code


@app.before_request
def setup_logger():
    """Setup operation context and logger context."""
    # Record request info in global context.
    g.method = request.method
    g.url = request.url
    g.entry_time = datetime.utcnow()

    # Setup operation context.
    runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
    runtime.update_operation_context(request)

    # Set logger context.
    custom_dimensions = get_custom_dimensions()
    for handler in logger.handlers:
        if isinstance(handler, TelemetryLogHandler):
            handler.set_or_update_context(custom_dimensions)

    # Set app insights instrumentation key.
    app_insights_key = request.headers.get("app-insights-instrumentation-key", None)
    if app_insights_key:
        set_app_insights_instrumentation_key(app_insights_key)
        system_logger.info("App insights instrumentation key is set.")
    else:
        system_logger.warning("App insights instrumentation key is missing in request header.")

    logger.info("Receiving request [method=%s] [url=%s]", g.method, g.url)


@app.after_request
def teardown_logger(response: Response):
    """Clear logger context."""
    duration_ms = (datetime.utcnow() - g.entry_time).total_seconds() * 1000  # Unit is milliseconds.
    logger.info(
        "Request finishes [status=%s] [duration(ms)=%s] [method=%s] [url=%s]",
        response.status_code,
        duration_ms,
        g.method,
        g.url,
    )

    for handler in logger.handlers:
        if isinstance(handler, TelemetryLogHandler):
            handler.flush()
            handler.clear()

    # Clear operation context.
    OperationContext.get_instance().clear()
    return response


def get_custom_dimensions() -> Dict[str, str]:
    """Get custom dimensions for telemetry log."""
    operation_context = OperationContext.get_instance()
    custom_dimensions = operation_context.get_context_dict()
    custom_dimensions.update({"host_name": os.environ.get("HOSTNAME", "")})  # Docker container name.
    return custom_dimensions


def generate_error_response(e):
    if isinstance(e, JsonSerializedPromptflowException):
        error_dict = json.loads(e.message)
    else:
        error_dict = ExceptionPresenter.create(e).to_dict(include_debug_info=True)

    logger.exception("Hit exception when execute request: \n{customer_content}", extra={"customer_content": e})

    # remove traceback from response
    error_dict.pop("debugInfo", None)

    return ErrorResponse.from_error_dict(error_dict)


@app.route("/submit_single_node", methods=["POST"])
@app.route("/aml-api/v1.0/submit_single_node", methods=["POST"])
def submit_single_node():
    """Process a single node request in the runtime."""
    runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
    req = SingleNodeRequestV2.deserialize(request.get_json())
    req_id = request.headers.get("x-ms-client-request-id")
    OperationContext.get_instance().run_mode = RunMode.SingleNode.name
    with get_log_context_from_v2_request(req):
        # Please do not change it, it is used to generate dashboard.
        logger.info(
            "[%s] Receiving v2 single node request %s: {customer_content}",
            req.flow_run_id,
            req_id,
            extra={"customer_content": req.desensitize_to_json()},
        )

        try:
            result = runtime.execute_flow(req, execute_node_request)
            logger.info("[%s] End processing single node", req.flow_run_id)

            return generate_response_from_run_result(result)
        except Exception as ex:
            _log_submit_request_exception(ex)
            raise ex


@app.route("/submit_single_node_async", methods=["POST"])
@app.route("/aml-api/v1.0/submit_single_node_async", methods=["POST"])
def submit_single_node_async():
    runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
    req = AsyncSingleNodeRequest.deserialize(request.get_json())
    try:
        if not req.is_default_variant and req.node_variant_id is None:
            raise NodeVariantInfoInvalid("It is invalid that is_default_variant is false and node_variant_id is None.")

        req_id = request.headers.get("x-ms-client-request-id")
        OperationContext.get_instance().run_mode = RunMode.SingleNode.name
        with get_log_context_from_v2_request(req), setup_contextvar(active_run_context, req):
            logger.info(
                "[%s] Receiving v2 async single node request %s: {customer_content}",
                req.flow_run_id,
                req_id,
                extra={"customer_content": req.desensitize_to_json()},
            )

            try:
                run_info: RunInfo = runtime.execute_flow(req, execute_async_node_request)
                logger.info("[%s] End processing v2 async single node request", req.flow_run_id)
                if run_info and run_info.error:
                    _log_error_response(ErrorResponse.from_error_dict(run_info.error))
                return jsonify({"message": "Async single node request completed."})
            except Exception as ex:
                _log_submit_request_exception(ex)
                raise ex
    except Exception as ex:
        logger.info("[%s] Update async single node %s to failed.", req.flow_run_id, req.node_name)
        _mark_async_run_as_failed(
            ex, req.flow_run_id, req.azure_storage_setting, req.node_name, req.is_default_variant, req.node_variant_id
        )
        raise


@app.route("/submit_flow", methods=["POST"])
@app.route("/aml-api/v1.0/submit_flow", methods=["POST"])
def submit_flow():
    runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
    req = FlowRequestV2.deserialize(request.get_json())
    req_id = request.headers.get("x-ms-client-request-id")
    OperationContext.get_instance().run_mode = RunMode.Test.name
    with get_log_context_from_v2_request(req):
        # Please do not change it, it is used to generate dashboard.
        logger.info(
            "[%s] Receiving v2 flow request %s: {customer_content}",
            req.flow_run_id,
            req_id,
            extra={"customer_content": req.desensitize_to_json()},
        )
        log_runtime_pf_version(logger)

        try:
            result = runtime.execute_flow(req, execute_flow_request)
            logger.info("[%s] End processing flow v2", req.flow_run_id)
            return generate_response_from_run_result(result)
        except Exception as ex:
            _log_submit_request_exception(ex)
            raise ex


@app.route("/submit_flow_async", methods=["POST"])
@app.route("/aml-api/v1.0/submit_flow_async", methods=["POST"])
def submit_flow_async():
    runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
    req = AsyncFlowRequest.deserialize(request.get_json())
    req_id = request.headers.get("x-ms-client-request-id")
    OperationContext.get_instance().run_mode = RunMode.Test.name
    with get_log_context_from_v2_request(req), setup_contextvar(active_run_context, req):
        logger.info(
            "[%s] Receiving v2 async flow request %s: {customer_content}",
            req.flow_run_id,
            req_id,
            extra={"customer_content": req.desensitize_to_json()},
        )
        log_runtime_pf_version(logger)

        try:
            run_info: FlowRunInfo = runtime.execute_flow(req, execute_async_flow_request)
            logger.info("[%s] End processing v2 async flow request", req.flow_run_id)
            if run_info and run_info.error:
                _log_error_response(ErrorResponse.from_error_dict(run_info.error))
            return jsonify({"message": "Async flow request completed."})
        except Exception as ex:
            _log_submit_request_exception(ex)
            logger.info("[%s] Update async flow run to failed.", req.flow_run_id)
            _mark_async_run_as_failed(ex, req.flow_run_id, req.azure_storage_setting)
            raise


@app.route("/submit_bulk_run", methods=["POST"])
@app.route("/aml-api/v1.0/submit_bulk_run", methods=["POST"])
def submit_bulk_run():
    runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
    OperationContext.get_instance().run_mode = RunMode.Batch.name
    payload = request.get_json()
    try:
        req: BulkRunRequestV2 = BulkRunRequestV2.deserialize(payload)
        req_id = request.headers.get("x-ms-client-request-id")
        with get_log_context_from_v2_request(req), setup_contextvar(active_run_context, req):
            # Please do not change it, it is used to generate dashboard.
            logger.info(
                "[%s] Receiving v2 bulk run request %s: {customer_content}",
                req.flow_run_id,
                req_id,
                extra={"customer_content": req.desensitize_to_json()},
            )
            log_runtime_pf_version(logger)
            mark_run_as_preparing_in_runhistory(runtime.config, req.flow_run_id)

            working_dir = None
            try:
                # Download snapshot and get language.
                working_dir: Path = get_working_dir_from_run_id(req.flow_run_id)
                download_snapshot(working_dir, runtime.config, req)
                lang = get_language(working_dir / req.flow_source.flow_dag_file)
                logger.info(f"About to execute a {lang} flow.")
                if lang == "csharp":
                    result: BatchResult = execute_csharp_bulk_run_request(runtime.config, req, working_dir)
                else:
                    result: BatchResult = runtime.execute_flow(req, execute_bulk_run_request)
                logger.info("[%s] End processing bulk run", req.flow_run_id)
                return generate_response_from_batch_result(result)
            except Exception as ex:
                _log_submit_request_exception(ex)
                raise ex
            finally:
                # remove working dir for bulk run
                if working_dir is not None:
                    logger.info("Cleanup working dir %s for bulk run", working_dir)
                    shutil.rmtree(working_dir, ignore_errors=True)
    except Exception as ex:
        runtime.mark_flow_runs_v2_as_failed(req, payload, ex)
        raise


@app.route("/cancel_run", methods=["POST"])
@app.route("/aml-api/v1.0/cancel_run", methods=["POST"])
def cancel_run():
    # Cancel async flow test or single node run.
    req = CancelRunRequest.deserialize(request.get_json())

    if req.azure_storage_setting is None:
        raise AzureStorageSettingMissing("Cancel async run needs azure_storage_setting.")
    with get_log_context_for_cancel_request(req):
        storage = AsyncRunStorage(run_id=req.flow_run_id, azure_storage_setting=req.azure_storage_setting)
        cancel_requested = storage.cancelling_run()
        if cancel_requested:
            return jsonify({"message": f"Set async run {req.flow_run_id} status to CancelRequested successfully."})
        else:
            return jsonify({"message": f"Async run {req.flow_run_id} may already completed."})


@app.route("/start_async_run", methods=["POST"])
@app.route("/aml-api/v1.0/start_async_run", methods=["POST"])
def start_async_run():
    # Create overview json and set status for async flow test or single node run as synchronous API.
    # Runtime internal API.
    # The request body will be AsyncFlowRequest or AsyncSingleNodeRequest.
    is_async_node_run = request.json.get("node_name") is not None
    if is_async_node_run:
        req = AsyncSingleNodeRequest.deserialize(request.get_json())
        with get_log_context_from_v2_request(req):
            storage = AsyncRunStorage(
                run_id=req.flow_run_id,
                azure_storage_setting=req.azure_storage_setting,
                is_default_variant=req.is_default_variant,
                node_variant_id=req.node_variant_id,
            )
            storage.start_node_run(req.node_name)
    else:
        req = AsyncFlowRequest.deserialize(request.get_json())
        with get_log_context_from_v2_request(req):
            storage = AsyncRunStorage(
                run_id=req.flow_run_id,
                azure_storage_setting=req.azure_storage_setting,
            )
            storage.start_flow_run()

    return jsonify({"message": "Start async run successful."})


def generate_response_from_run_result(result: dict):
    error_response: ErrorResponse = RunResultParser(result).get_error_response()
    if error_response:
        d = error_response.to_dict()
        result["errorResponse"] = d
        _log_error_response(error_response=error_response)

    resp = jsonify(result)

    return resp


def generate_response_from_batch_result(batch_result: BatchResult):
    if batch_result is not None and not isinstance(batch_result, BatchResult):
        system_logger.warning(f"batch_result is not BatchResult type: {type(batch_result)}")
        return jsonify(dict())

    if batch_result is None or batch_result.error_summary is None:
        return jsonify(dict())

    # We should first check batch run level error, and then check each line error.
    if hasattr(batch_result.error_summary, "batch_error_dict") and batch_result.error_summary.batch_error_dict:
        error_response: ErrorResponse = ErrorResponse.from_error_dict(batch_result.error_summary.batch_error_dict)
    else:
        error_list = batch_result.error_summary.error_list
        if error_list is None or len(error_list) == 0:
            return jsonify(dict())
        # Only use first error to generate error response.
        error_response: ErrorResponse = ErrorResponse.from_error_dict(error_list[0].error)

    d = error_response.to_dict()
    result = {"errorResponse": d}
    _log_error_response(error_response=error_response)
    return jsonify(result)


def _log_error_response(error_response: ErrorResponse):
    d = error_response.to_dict()
    _log_submit_request_error_response(error_response)
    stack_trace = generate_safe_error_stacktrace(d)
    system_logger.warning(f"Log run error stack trace: \n{stack_trace}")


@app.route("/aml-api/v1.0/package_tools")
@app.route("/package_tools")
def package_tools():
    import imp

    import pkg_resources

    imp.reload(pkg_resources)
    return jsonify(collect_package_tools())


@app.route("/aml-api/v1.0/dynamic_list", methods=["POST"])
@app.route("/dynamic_list", methods=["POST"])
def dynamic_list():
    from promptflow._internal import gen_dynamic_list

    logger.info(
        "Receiving dynamic_list request: payload = {customer_content}", extra={"customer_content": request.json}
    )
    func_path = request.json.get("func_path", "")
    func_kwargs = request.json.get("func_kwargs", {})

    # May call azure control plane api in the custom function to list Azure resources.
    # which may need Azure workspace triple.
    runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
    ws_triple = {
        "subscription_id": runtime.config.deployment.subscription_id,
        "resource_group_name": runtime.config.deployment.resource_group,
        "workspace_name": runtime.config.deployment.workspace_name,
    }
    result = gen_dynamic_list(func_path, func_kwargs, ws_triple)
    logger.info(
        "dynamic list request finished. Result: {customer_content}",
        extra={"customer_content": str(result)},
    )
    return jsonify(result)


@app.route("/aml-api/v1.0/retrieve_tool_func_result", methods=["POST"])
@app.route("/retrieve_tool_func_result", methods=["POST"])
def retrieve_tool_func_result():
    from promptflow._internal import retrieve_tool_func_result

    payload = request.json
    logger.info(
        "Receiving retrieve_tool_func_result request: payload = {customer_content}", extra={"customer_content": payload}
    )

    func_path = payload.get("func_path", "")
    func_kwargs = payload.get("func_kwargs", {})
    func_call_scenario = payload.get("func_call_scenario", "")

    # May call azure control plane api in the custom function to list Azure resources.
    # which may need Azure workspace triple.
    runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
    ws_triple = {
        "subscription_id": runtime.config.deployment.subscription_id,
        "resource_group_name": runtime.config.deployment.resource_group,
        "workspace_name": runtime.config.deployment.workspace_name,
    }

    func_result = retrieve_tool_func_result(func_call_scenario, func_path, func_kwargs, ws_triple)

    logger.info(
        "Retrieve_tool_func_result request finished. Result: {customer_content}",
        extra={"customer_content": str(func_result)},
    )

    resp = {"result": func_result, "logs": {}}
    return jsonify(resp)


# S2S calls for CI need prefix "/aml-api/v1.0"
@app.route("/aml-api/v1.0/meta-v2/", methods=["POST"])
@app.route("/meta-v2", methods=["POST"])
def meta_v2():
    # Get parameters and payload
    logger.info("Receiving v2 meta request: payload = {customer_content}", extra={"customer_content": request.json})
    data = MetaV2Request.deserialize(request.json)
    runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
    if data.flow_source_type == FlowSourceType.AzureFileShare:
        runtime_dir = fill_working_dir(
            runtime.config.deployment.compute_type, data.flow_source_info, "meta_%s" % uuid.uuid4()
        )
    elif data.flow_source_type == FlowSourceType.DataUri:
        runtime_dir = Path("requests", "meta_%s" % uuid.uuid4()).resolve()

        logger.info(
            "Preparing flow directory for dataUri: {customer_content}",
            extra={"customer_content": data.flow_source_info.data_uri},
        )
        prepare_blob_directory(data.flow_source_info.data_uri, runtime_dir, runtime_config=runtime.config)
    else:
        raise InvalidFlowSourceType(
            message_format="Invalid flow_source_type value for MetaV2Request: {flow_source_type}",
            flow_source_type=data.flow_source_type,
        )
    logger.info("Generate meta_v2 in runtime_dir {customer_content}", extra={"customer_content": runtime_dir})
    manager = multiprocessing.Manager()
    tool_dict = manager.dict()
    exception_dict = manager.dict()
    custom_dimensions = get_custom_dimensions()
    # TODO: Use spawn method to start child process, not fork.
    p = multiprocessing.Process(
        target=generate_metas_from_files, args=(data.tools, runtime_dir, tool_dict, exception_dict, custom_dimensions)
    )
    p.start()
    p.join(timeout=SYNC_REQUEST_TIMEOUT_THRESHOLD)
    if p.is_alive():
        logger.info(f"Stop generating meta for exceeding {SYNC_REQUEST_TIMEOUT_THRESHOLD} seconds.")
        p.terminate()
        p.join()

    resp_tools = {source: tool for source, tool in tool_dict.items()}
    # exception_dict was created by manager.dict(), so convert to a normal dict here.
    resp_errors = {source: exception for source, exception in exception_dict.items()}
    # For not processed tools, treat as timeout error.
    for source in data.tools.keys():
        if source not in resp_tools and source not in resp_errors:
            resp_errors[source] = generate_error_response(
                GenerateMetaTimeout(message_format="Generate meta timeout for source '{source}'.", source=source)
            ).to_dict()
    resp = {"tools": resp_tools, "errors": resp_errors}
    return jsonify(resp)


@app.route("/v1.0/Connections/<string:name>/listsecrets")
def get_connection(name: str):
    logger.info(f"Retrieving connection with name = {name}")
    runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
    config = runtime.config
    try:
        connection_dict = build_connection_dict(
            [name],
            config.deployment.subscription_id,
            config.deployment.resource_group,
            config.deployment.workspace_name,
        )
    except OpenURLNotFoundError as ex:
        return jsonify(generate_error_response(ex).to_dict()), 404

    result = connection_dict.get(name)
    if result is None or result.get("value") is None:
        raise Exception("connection or its value is None.")

    # Reformat response to align with the response of local pfs server.
    def _convert_connection_type(input_connection_type: str) -> str:
        """Convert to snake case and remove suffix if exists."""
        suffix_to_remove = "_connection"
        input_connection_type = to_snake_case(input_connection_type)
        if input_connection_type.endswith(suffix_to_remove):
            return input_connection_type[: -len(suffix_to_remove)]
        return input_connection_type

    response = result.get("value")
    response.update(
        {"name": name, "type": _convert_connection_type(result.get("type", "")), "module": result.get("module")}
    )
    return jsonify(response)


def generate_tool_meta_dict_by_file_allow_non_py(source, tool_type: str = "python"):
    tool_type = ToolType(tool_type)
    if tool_type == ToolType.PYTHON and not source.endswith(".py"):
        # For non-python file, we may rename it and try,
        # this is because UX will prepare another temp file without .py suffix.
        updated_source = source + ".tmp.py"
        os.rename(source, updated_source)
        return generate_tool_meta_dict_by_file(updated_source, tool_type)
    return generate_tool_meta_dict_by_file(source, tool_type)


def generate_metas_from_files(tools, runtime_dir, tool_dict, exception_dict, custom_dimensions):
    # Reinitialize logger in child process.
    with reset_and_close_logger(), set_custom_dimensions_to_logger(logger, custom_dimensions), _change_working_dir(
        runtime_dir
    ), inject_sys_path(runtime_dir):
        for source, config in tools.items():
            try:
                if "tool_type" not in config:
                    raise NoToolTypeDefined(
                        message_format="Tool type not defined for source '{source}'.", source=source
                    )
                tool_type = config.get("tool_type", ToolType.PYTHON)
                tool_dict[source] = generate_tool_meta_dict_by_file_allow_non_py(source, tool_type)
            except Exception as e:
                exception_dict[source] = generate_error_response(e).to_dict()


@app.route("/aml-api/v1.0/health", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    """Check if the runtime is alive."""
    return {"status": "Healthy", "version": VERSION}


@app.route("/aml-api/v1.0/version", methods=["GET"])
@app.route("/version", methods=["GET"])
def version():
    """Check the runtime's version."""
    build_info = os.environ.get("BUILD_INFO", "")
    try:
        build_info_dict = json.loads(build_info)
        version = build_info_dict["build_number"]
    except Exception:
        version = VERSION
    feature_list = get_total_feature_list()  # get current feature list of both runtime and executor
    api_list = get_runtime_api_list()  # get current runtime api list
    logger.info(f"Build info: {build_info}. Version: {version}. Feature list: {feature_list}. Api list: {api_list}.")
    return {
        "status": "Healthy",
        "build_info": build_info,
        "version": version,
        "feature_list": feature_list,
        "api_list": api_list,
    }


def generate_meta_multiprocessing(content, name, tool_type, return_dict, exception_queue):
    """Generate meta data unbder isolated process.
    Note: do not change order of params since it will be used in multiprocessing executor.
    """
    with multi_processing_exception_wrapper(exception_queue):
        if tool_type == ToolType.LLM:
            result = generate_prompt_meta(name, content)
        elif tool_type == ToolType.PROMPT:
            result = generate_prompt_meta(name, content, prompt_only=True)
        else:
            result = generate_python_meta(name, content)
        return_dict["result"] = result


def create_app(config="prt.yaml", args=None):
    """Create a flask app."""
    register_signal_handler()
    config = Path(config).absolute()
    logger.info("Init runtime with config file in create_app: %s", config)
    config = load_runtime_config(config, args=args)
    PromptFlowRuntime.init(config)
    logger.info("Finished init runtime with config file in create_app.")
    return app


def _log_submit_request_exception(ex: Exception):
    resp: ErrorResponse = generate_error_response(ex)
    _log_submit_request_error_response(resp)


def _log_submit_request_error_response(resp: ErrorResponse):
    """Please do not change the texts, because they are used to generate dashboard."""
    logger.error(
        (
            "Submit flow request failed "
            f"Code: {resp.response_code} "
            f"InnerException type: {resp.innermost_error_code} "
            f"Exception type hierarchy: {resp.error_code_hierarchy}"
        )
    )


def _mark_async_run_as_failed(
    ex: Exception,
    flow_run_id: str,
    azure_storage_setting: AzureStorageSetting,
    single_node_name: str = None,
    is_default_variant: bool = True,
    node_variant_id: str = None,
):
    error_response = ErrorResponse.from_exception(ex)
    if single_node_name:
        storage = AsyncRunStorage(
            run_id=flow_run_id,
            azure_storage_setting=azure_storage_setting,
            is_default_variant=is_default_variant,
            node_variant_id=node_variant_id,
        )
        storage.fail_node_run(node=single_node_name, error_response=error_response.to_dict())
    else:
        storage = AsyncRunStorage(
            run_id=flow_run_id,
            azure_storage_setting=azure_storage_setting,
        )
        storage.fail_flow_run(error_response=error_response.to_dict())


if __name__ == "__main__":
    PromptFlowRuntime.get_instance().init_logger()
    app.run()
