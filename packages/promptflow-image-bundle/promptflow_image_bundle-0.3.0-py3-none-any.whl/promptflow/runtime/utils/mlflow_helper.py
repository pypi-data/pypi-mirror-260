import json
import os
from datetime import datetime
from typing import Dict, List

from promptflow._internal import ErrorResponse, RootErrorCode, bulk_logger
from promptflow.contracts.run_info import FlowRunInfo
from promptflow.contracts.run_info import Status as PromptflowRunStatus
from promptflow.exceptions import ErrorTarget, SystemErrorException, UserErrorException
from promptflow.runtime._errors import FailedToGetHostCreds, InvalidClientAuthentication, to_string
from promptflow.runtime.utils import logger
from promptflow.runtime.utils._debug_log_helper import generate_safe_error_stacktrace
from promptflow.runtime.utils._utils import is_in_ci_pipeline
from promptflow.runtime.utils.internal_logger_utils import system_logger
from promptflow.runtime.utils.retry_utils import retry
from promptflow.runtime.utils.timer import Timer

try:
    import mlflow
    from azure.core.exceptions import ClientAuthenticationError
    from mlflow.entities.run import Run as MlflowRun
    from mlflow.entities.run_status import RunStatus as MlflowRunStatus
    from mlflow.exceptions import RestException
    from mlflow.protos.databricks_pb2 import RESOURCE_DOES_NOT_EXIST, ErrorCode
    from mlflow.tracking import MlflowClient
    from mlflow.utils.rest_utils import http_request
except ImportError as e:
    msg = f"Please install azure-related packages, currently got {str(e)}"
    raise UserErrorException(message=msg, target=ErrorTarget.AZURE_RUN_STORAGE)

RunStatusMapping = {
    PromptflowRunStatus.Completed.value: MlflowRunStatus.to_string(MlflowRunStatus.FINISHED),
    PromptflowRunStatus.Failed.value: MlflowRunStatus.to_string(MlflowRunStatus.FAILED),
    PromptflowRunStatus.Canceled.value: MlflowRunStatus.to_string(MlflowRunStatus.KILLED),
}


class MlflowHelper:
    ERROR_EVENT_NAME = "Microsoft.MachineLearning.Run.Error"
    ERROR_MESSAGE_SET_MULTIPLE_TERMINAL_STATUS = "Cannot set run to multiple terminal states"
    RUN_HISTORY_TOTAL_TOKENS_PROPERTY_NAME = "azureml.promptflow.total_tokens"

    def __init__(self, mlflow_tracking_uri):
        """Set mlflow tracking uri to target uri"""
        self.enable_usage_in_ci_pipeline_if_needed()
        if isinstance(mlflow_tracking_uri, str) and mlflow_tracking_uri.startswith("azureml:"):
            logger.info(f"Setting mlflow tracking uri to {mlflow_tracking_uri!r}")
            mlflow.set_tracking_uri(mlflow_tracking_uri)
        else:
            message = (
                f"Mlflow tracking uri must be a string that starts with 'azureml:', "
                f"got {mlflow_tracking_uri!r} with type {type(mlflow_tracking_uri)!r}."
            )
            raise UserErrorException(message=message, target=ErrorTarget.AZURE_RUN_STORAGE)

        self.client = MlflowClient()
        self.api_call_cred = self.get_api_call_cred()

    def get_api_call_cred(self):
        try:
            # modify client cred to be used in run history api call
            api_call_cred = self.get_host_creds()
            api_call_cred.host = api_call_cred.host.replace("mlflow/v2.0", "mlflow/v1.0").replace(
                "mlflow/v1.0", "history/v1.0"
            )

            return api_call_cred
        except ClientAuthenticationError as ex:
            raise InvalidClientAuthentication(message="Failed to get mlflow credential") from ex
        except Exception as e:
            ex_message = to_string(e)
            error_message = f"Failed to get host creds with error {ex_message}."
            logger.error(error_message)
            raise FailedToGetHostCreds(
                message=error_message,
                target=ErrorTarget.AZURE_RUN_STORAGE,
            ) from e

    # mlflow client get credential may return ClientAuthenticationError transiently even with correct credential
    @retry(ClientAuthenticationError, tries=5, delay=0.5, backoff=1, logger=logger)
    def get_host_creds(self):
        return self.client._tracking_client.store.get_host_creds()

    def enable_usage_in_ci_pipeline_if_needed(self):
        if is_in_ci_pipeline():
            # this is to enable mlflow use CI SP client credential
            # Refer to: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-mlflow-configure-tracking?view=azureml-api-2&tabs=python%2Cmlflow#configure-authentication  # noqa: E501
            os.environ["AZURE_TENANT_ID"] = os.environ.get("tenantId")
            os.environ["AZURE_CLIENT_ID"] = os.environ.get("servicePrincipalId")
            os.environ["AZURE_CLIENT_SECRET"] = os.environ.get("servicePrincipalKey")

    def check_run_isactive(self, run_id: str):
        run: MlflowRun = mlflow.active_run()
        return run is not None and run.info.run_id == run_id

    def start_run(self, run_id: str, create_if_not_exist: bool = False):
        try:
            logger.info(
                f"Starting the aml run {run_id!r}...",
            )
            mlflow.start_run(run_id=run_id)
        except Exception as e:
            msg = str(e)
            if (
                create_if_not_exist
                and isinstance(e, RestException)
                and e.error_code == ErrorCode.Name(RESOURCE_DOES_NOT_EXIST)
            ):
                logger.warning(f"Run {run_id!r} not found, will create a new run with this run id.")
                self.create_run(run_id=run_id)
                return
            raise SystemErrorException(
                f"Failed to start root run {run_id!r} in workspace through mlflow: {msg}",
                target=ErrorTarget.AZURE_RUN_STORAGE,
                error=e,
            )

    def create_run(self, run_id: str, start_after_created=True, backoff_factor=None):
        """Create a run with specified run id"""
        endpoint = "/experiments/{}/runs/{}".format("Default", run_id)
        json_obj = {"runId": run_id}
        response = http_request(
            host_creds=self.api_call_cred,
            endpoint=endpoint,
            method="PATCH",
            json=json_obj,
            backoff_factor=backoff_factor,
        )

        if response.status_code == 401:
            logger.info(f"Original credential is expired, get a new credential and create the run {run_id!r} again...")
            self.api_call_cred = self.get_api_call_cred()
            response = http_request(
                host_creds=self.api_call_cred,
                endpoint=endpoint,
                method="PATCH",
                json=json_obj,
                backoff_factor=backoff_factor,
            )

        if response.status_code == 200:
            if start_after_created:
                try:
                    mlflow.start_run(run_id=run_id)
                except Exception as e:
                    raise SystemErrorException(
                        f"A new run {run_id!r} is created but failed to start it: {str(e)}",
                        target=ErrorTarget.AZURE_RUN_STORAGE,
                    )
        else:
            raise SystemErrorException(
                f"Failed to create run {run_id!r}: {response.text}",
                target=ErrorTarget.AZURE_RUN_STORAGE,
            )

    def end_aml_root_run(self, run_id: str, status: str, error_response: Dict = None) -> None:
        if error_response:
            try:
                # Start run otherwise mlflow.active_run() will return None.
                # TODO: Remove the try/catch if the warning message is not found in the system log.
                if not self.check_run_isactive(run_id):
                    self.start_run(run_id, True)
            except Exception as e:
                system_logger.warning(f"Failed to start run. Exception: {e}")
            current_run = self.get_run(run_id)
            self.write_error_message(mlflow_run=current_run, error_response=error_response)
        self.end_run(run_id=run_id, status=status)

    def end_run(self, run_id: str, status: str):
        """Update root run to end status"""
        if status not in RunStatusMapping:
            raise SystemErrorException(
                message="Trying to end a workspace root run with non-terminated status.",
                target=ErrorTarget.AZURE_RUN_STORAGE,
            )
        mlflow_status = RunStatusMapping[status]

        try:
            logger.info(
                f"Ending the aml run {run_id!r} with status {status!r}...",
            )
            mlflow.end_run(status=mlflow_status)
        except Exception as e:
            if isinstance(e, RestException) and self.ERROR_MESSAGE_SET_MULTIPLE_TERMINAL_STATUS in e.message:
                logger.warning(f"Failed to set run {run_id!r} to {status!r} since it is already ended.")
                return
            raise SystemErrorException(
                f"Failed to end root run {run_id!r} in workspace through mlflow: {str(e)}",
                target=ErrorTarget.AZURE_RUN_STORAGE,
                error=e,
            )

    def get_safe_tool_execution_error_response(self, run_info_error: dict) -> dict:
        """Get safe tool execution error message for user tool execution error"""
        response = ErrorResponse.from_error_dict(run_info_error)
        if response.error_code_hierarchy != "UserError/ToolExecutionError":
            return response.to_dict()

        copy_error_info = dict(run_info_error)
        if "message" in copy_error_info:
            copy_error_info["message"] = self._get_safe_tool_execution_error_message(copy_error_info)
        return ErrorResponse.from_error_dict(copy_error_info).to_dict()

    def overwrite_cloud_batch_error_message(self, run_info_error: dict):
        """Cloud mode we may has different error message with local mode, so we need to overwrite it."""
        response = ErrorResponse.from_error_dict(run_info_error)
        if response.error_code_hierarchy != "UserError/BatchRunTimeoutError":
            return

        batch_timeout_error_message = (
            "A timeout has occurred. Batch runs have a maximum limit of 10 hours. "
            "Please ensure you are not throttled by LLM capacity, "
            "consider reducing your data size, or contact product team via feedback or support request."
        )
        if "message" in run_info_error:
            run_info_error["message"] = batch_timeout_error_message

        return

    def _get_safe_tool_execution_error_message(self, error_info: dict) -> str:
        """
        Get safe tool execution error message

        Example dict:
        {
            "code": "UserError",
            "severity": null,
            "message": "Execution failure in 'print_input_tool': (Exception) Hello world",
            "messageParameters": {
                "node_name": "print_input_tool"
            },
            "referenceCode": "Tool/__pf_main__",
            "detailsUri": null,
            "target": null,
            "details": [],
            "innerError": {
                "code": "ToolExecutionError",
                "innerError": null
            }
        }
        """

        scrubbed_patter = "**Error message scrubbed**"
        if "messageParameters" in error_info:
            message_parameters = error_info["messageParameters"]
            if isinstance(message_parameters, dict) and "node_name" in message_parameters:
                node_name = message_parameters["node_name"]
                if node_name:
                    return f"Execution failure in '{node_name}'. (Execution) " + scrubbed_patter

        return error_info.get("message", "")

    def get_run(self, run_id: str):
        return mlflow.get_run(run_id=run_id)

    def active_run(self):
        """Get current active run"""
        return mlflow.active_run()

    def write_error_message(self, mlflow_run: MlflowRun, error_response: dict):
        """Write error message to run history with specified exception info"""
        run_id = mlflow_run.info.run_id
        experiment_id = mlflow_run.info.experiment_id
        logger.warning(f"[{run_id}] Run failed. Execution stackTrace: {generate_safe_error_stacktrace(error_response)}")

        error_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "name": self.ERROR_EVENT_NAME,
            "data": {
                "errorResponse": error_response,
            },
        }

        endpoint = "/experimentids/{}/runs/{}/events".format(experiment_id, run_id)
        response = http_request(
            host_creds=self.api_call_cred,
            endpoint=endpoint,
            method="POST",
            json=error_event,
        )

        if response.status_code == 401:
            logger.info(
                f"Original credential is expired, get a new credential "
                f"and write error message for run {run_id!r} again..."
            )
            self.api_call_cred = self.get_api_call_cred()
            response = http_request(
                host_creds=self.api_call_cred,
                endpoint=endpoint,
                method="POST",
                json=error_event,
            )

        if response.status_code != 200:
            message = (
                f"Failed to write error message to run history for run {run_id!r}, response status code: "
                f"{response.status_code!r}, response message: {response.text!r}"
            )
            logger.warning(message)

    def generate_properties(self, system_metrics: Dict):
        return {
            # Write total_tokens into RH (RunDto.Properties), For example, "azureml.promptflow.total_tokens": "12"
            # System_metrics["total_tokens"] is integer. We write 0 if this metrics not exist
            self.RUN_HISTORY_TOTAL_TOKENS_PROPERTY_NAME: system_metrics.get("total_tokens", 0),
            # Add instance_results.jsonl path to run properties. Which is required by UI feature.
            "_azureml.evaluate_artifacts": '[{"path": "instance_results.jsonl", "type": "table"}]',
        }

    def update_run_history_properties_from_run_info(self, run_info: FlowRunInfo):
        properties = self.generate_properties(run_info.system_metrics)
        self.update_run_history_properties(properties)

    def update_run_history_properties(self, properties: Dict):
        current_run = mlflow.active_run()
        if not current_run:
            # warning when there is no active aml run, not raise exception in case the issue is from mlflow itself.
            logger.warning("No active aml run found, make sure run tracker has started a aml run")
            return

        run_id = current_run.info.run_id
        # run_info does not have experiment_id, so we get from current_run from mflow
        experiment_id = current_run.info.experiment_id
        with Timer(bulk_logger, "Upload RH properties for run " + run_id):
            endpoint = "/experimentids/{}/runs/{}".format(experiment_id, run_id)
            json_obj = {"runId": run_id, "properties": properties}
            response = http_request(
                host_creds=self.api_call_cred,
                endpoint=endpoint,
                method="PATCH",
                json=json_obj,
            )

            if response.status_code == 401:
                logger.info(
                    f"Original credential is expired, get a new credential "
                    f"and write run properties for run {run_id!r} again..."
                )
                self.api_call_cred = self.get_api_call_cred()
                response = http_request(
                    host_creds=self.api_call_cred,
                    endpoint=endpoint,
                    method="PATCH",
                    json=json_obj,
                )

            if response.status_code == 200:
                logger.info(f"Successfully write run properties {json.dumps(properties)} with run id '{run_id}'")
            else:
                logger.warning(
                    f"Failed to write run properties {json.dumps(properties)} with run id {run_id}. "
                    f"Code: {response.status_code}, text: {response.text}"
                )

    def upload_metrics_to_run_history(self, run_id: str, metrics: Dict):
        if isinstance(metrics, dict) and len(metrics) > 0:
            # There should be a root aml run that was created by MT when we try to log metrics for.
            # Run tracker will start this aml run when executing the flow run and here we should get the active run.
            current_run = mlflow.active_run()
            if not current_run:
                # warning when there is no active aml run, not raise exception in case the issue is from mlflow itself.
                logger.warning(
                    "No active aml run found, make sure run tracker has started a aml run to log metrics for."
                )
                return

            # start to log metrics to aml run
            # TODO: Refine the logic here since log_metric logic should handled in runtime bulk api instead of here
            with Timer(bulk_logger, "Upload metrics for run " + run_id):
                try:
                    for metric_name, value in metrics.items():
                        # use mlflow api to upload refined metric
                        mlflow.log_metric(metric_name, value)
                except Exception as e:
                    logger.warning(f"Failed to upload metrics to workspace: {str(e)}")
        elif metrics is not None and not isinstance(metrics, dict):
            logger.warning(f"Metrics should be a dict but got a {type(metrics)!r} with content {metrics!r}")

    def persist_status_summary(self, metrics: dict, flow_run_id: str):
        """Upload status summary metrics to run history via mlflow"""
        if isinstance(metrics, dict) and len(metrics) > 0:
            # There should be a root aml run that was created by MT when we try to log metrics for.
            # Run tracker will start this aml run when executing the flow run and here we should get the active run.
            current_run = mlflow.active_run()
            if not current_run:
                # warning when there is no active aml run, not raise exception in case the issue is from mlflow itself.
                logger.warning(
                    "No active aml run found, make sure run tracker has started a aml run to log metrics for."
                )
                return

            # start to log metrics to aml run
            with Timer(bulk_logger, "Upload status summary metrics for run " + flow_run_id):
                try:
                    for metric_name, value in metrics.items():
                        # use mlflow api to status summary inner metric
                        mlflow.log_metric(metric_name, value)
                except Exception as e:
                    logger.warning(f"Failed to upload status summary metrics to workspace: {str(e)}")
        elif metrics is not None and not isinstance(metrics, dict):
            logger.warning(f"Metrics should be a dict but got a {type(metrics)!r} with content {metrics!r}")


def _validate_error_details(error_list):
    """
    Make sure error details json string size is less than 1.6 million characters. Truncate the error detail
    to not exceed the limit if needed.
    """
    MAX_JSON_STRING_SIZE = 1600000
    while len(json.dumps(error_list)) > MAX_JSON_STRING_SIZE:
        old_length = len(error_list)
        new_length = old_length // 2
        error_list = error_list[:new_length]
        logger.warning(
            f"Error details json string size exceeds limit {MAX_JSON_STRING_SIZE!r}, "
            f"truncated error details item count from {old_length!r} to {new_length!r}."
        )

    return error_list


def generate_error_dict_for_root_run(
    error_list: List[Dict],
    total_lines_count: int,
) -> Dict:
    """Generate error response for root run

    error_list: list of error dict of a child flow run.
    """

    user_error_list = [error for error in error_list if error["code"] == RootErrorCode.USER_ERROR]
    system_error_list = [error for error in error_list if error["code"] == RootErrorCode.SYSTEM_ERROR]

    root_run_error = dict()
    if len(user_error_list) > 0:
        root_run_error = user_error_list[0]
    if len(system_error_list) > 0:
        root_run_error = system_error_list[0]

    error_details = dict()
    for error in error_list:
        # use error code and error message as key to aggregate
        error_key = error["code"] + error.get("messageFormat", "")
        if error_key not in error_details:
            error_details[error_key] = {
                "code": ErrorResponse(error).error_code_hierarchy,
                "messageFormat": error.get("messageFormat", ""),
                "count": 1,
            }
        else:
            error_details[error_key]["count"] += 1

    # update root run error message with aggregated error details
    if error_details:
        # there is a hard limitation for writing run history error message which is 3000 characters
        # so we use "messageFormat" to store the full error message, the limitation for "messageFormat"
        # is between 1.6 million and 3.2 million characters
        root_run_error["messageFormat"] = json.dumps(
            {
                "totalChildRuns": total_lines_count,
                "userErrorChildRuns": len(user_error_list),
                "systemErrorChildRuns": len(system_error_list),
                "errorDetails": _validate_error_details(list(error_details.values())),
            }
        )
    return root_run_error
