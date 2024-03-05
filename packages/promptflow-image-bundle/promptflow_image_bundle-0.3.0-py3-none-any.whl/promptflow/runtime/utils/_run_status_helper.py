from azure.core.exceptions import ClientAuthenticationError

from promptflow._internal import ErrorResponse
from promptflow.contracts.run_info import Status
from promptflow.runtime._errors import InvalidClientAuthentication
from promptflow.runtime.runtime_config import RuntimeConfig

from . import logger


def mark_run_v2_as_failed_in_runhistory(config: RuntimeConfig, flow_run_id, ex: Exception):
    from promptflow.runtime.utils.mlflow_helper import MlflowHelper

    mlflow_tracking_uri = config.set_mlflow_tracking_uri()
    mlflow_helper = MlflowHelper(mlflow_tracking_uri=mlflow_tracking_uri)

    try:
        logger.info(f"Start to update bulk run v2 {flow_run_id} status to Failed.")
        if not mlflow_helper.check_run_isactive(flow_run_id):
            mlflow_helper.start_run(flow_run_id, True)
        mlflow_run = mlflow_helper.get_run(run_id=flow_run_id)
        error_response = ErrorResponse.from_exception(ex).to_dict()
        mlflow_helper.write_error_message(mlflow_run=mlflow_run, error_response=error_response)
        mlflow_helper.end_run(flow_run_id, Status.Failed.value)
        logger.info(f"End to update bulk run {flow_run_id} status to Failed.")
    except Exception as exception:
        logger.warning(
            "Hit exception when update bulk run v2 %s status to Failed in run history, exception: %s",
            flow_run_id,
            exception,
        )


def mark_run_as_preparing_in_runhistory(config: RuntimeConfig, flow_run_id: str):
    from promptflow.runtime.utils._run_history_client import RunNotFoundError

    try:
        run_history_client = config.get_run_history_client()
        try:
            run = run_history_client.get_run(flow_run_id)
        except ClientAuthenticationError as ex:
            raise InvalidClientAuthentication(message="Failed to get run from runhistory") from ex
        except RunNotFoundError:
            from promptflow.runtime.utils.mlflow_helper import MlflowHelper

            mlflow_tracking_uri = config.set_mlflow_tracking_uri()
            mlflow_helper = MlflowHelper(mlflow_tracking_uri=mlflow_tracking_uri)
            logger.info(f"Flow run {flow_run_id} not exists. create one")
            mlflow_helper.create_run(flow_run_id, False)
            run = run_history_client.get_run(flow_run_id)
        if run.get("status", "") == Status.NotStarted.value:
            run_history_client.update_run_status(flow_run_id, Status.Preparing)
        else:
            logger.info(f"Flow run {flow_run_id} status is {run.get('status', '')}")
    except Exception as exception:
        logger.warning(
            "Hit exception when update bulk run v2 %s status to Preparing in run history, exception: %s",
            flow_run_id,
            exception,
        )
