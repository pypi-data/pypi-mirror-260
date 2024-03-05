import json
import os
import shutil
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Union

from azure.core.exceptions import ResourceModifiedError

from promptflow._internal import flow_logger, persist_multimedia_data
from promptflow.contracts.run_info import FlowRunInfo, RunInfo, Status
from promptflow.exceptions import ErrorTarget, UserErrorException
from promptflow.runtime._errors import (
    AzureStorageOperationError,
    AzureStorageUserError,
    StorageAuthenticationError,
    UserAuthenticationError,
)
from promptflow.runtime.constants import LINE_NUMBER_KEY, STATUS_KEY, PromptflowEdition
from promptflow.runtime.contracts.azure_storage_setting import AzureStorageSetting
from promptflow.runtime.storage.run_storage import AbstractRunStorage
from promptflow.runtime.utils import logger
from promptflow.runtime.utils._artifact_client import ArtifactClient
from promptflow.runtime.utils._asset_client import AssetClient
from promptflow.runtime.utils._run_history_client import OutputAssetInfo
from promptflow.runtime.utils._utils import get_default_credential
from promptflow.runtime.utils.mlflow_helper import MlflowHelper
from promptflow.runtime.utils.retry_utils import retry
from promptflow.runtime.utils.timer import Timer
from promptflow.storage.run_records import LineRunRecord, NodeRunRecord

try:
    from azure.ai.ml._azure_environments import EndpointURLS, _get_cloud, _get_default_cloud_name
    from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError
    from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
except ImportError as e:
    msg = f"Please install azure-related packages, currently got {str(e)}"
    raise UserErrorException(message=msg, target=ErrorTarget.AZURE_RUN_STORAGE)


class StorageOperations(Enum):
    UPDATE = "update"
    CREATE = "create"


class RuntimeAuthErrorType:
    WORKSPACE = "workspace"
    STORAGE = "storage"


def blob_error_handling_decorator(func):
    @retry(ResourceExistsError, tries=5)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ResourceExistsError as e:
            # raise original ResourceExistsError and retry if it's BlobModifiedWhileReading error,
            # this is a known issue of ADLS Gen2 storage and it's suggested to retry,
            # see https://github.com/Azure/azure-sdk-for-python/issues/26126 for more details.
            # for other cases, raise AzureStorageUserError.
            if e.status_code == 409 and "BlobModifiedWhileReading" in e.message:
                raise

            original_msg = str(e)
            refined_error_msg = (
                "Failed to upload write to blob because trying to "
                "create a new blob with an existing name. "
                f"Original error: {original_msg}"
            )
            logger.error(refined_error_msg)
            raise AzureStorageUserError(
                message=refined_error_msg,
                target=ErrorTarget.AZURE_RUN_STORAGE,
            ) from e
        except ClientAuthenticationError as e:
            msg = str(e)
            auth_error_msg = (
                "Failed to perform azure blob operation due to no available identity, please authenticate "
                f"the compute with proper identity. Original error: {msg}"
            )
            logger.error(auth_error_msg)
            raise StorageAuthenticationError(
                message=auth_error_msg,
                target=ErrorTarget.AZURE_RUN_STORAGE,
            ) from e
        except HttpResponseError as e:
            msg = str(e)
            if e.status_code == 403:
                auth_error_msg = (
                    "Failed to perform azure blob operation due to invalid authentication, please assign RBAC role "
                    f"'Storage Blob Data Contributor' to the service principal or client. Original error: {msg}"
                )
                logger.error(auth_error_msg)
                raise StorageAuthenticationError(
                    message=auth_error_msg,
                    target=ErrorTarget.AZURE_RUN_STORAGE,
                ) from e
            raise
        except Exception as e:
            original_msg = str(e)
            refined_error_msg = f"Failed to upload run info to blob. Original error: {original_msg}"
            logger.error(refined_error_msg)
            raise AzureStorageOperationError(
                message=refined_error_msg,
                target=ErrorTarget.AZURE_RUN_STORAGE,
            ) from e

    return wrapper


@blob_error_handling_decorator
def append_blob(blob_client: BlobClient, append_content: str):
    """Try append azure blob and handle the exceptions"""
    # note all auth related error are already handled in the constructor
    # Do not use blob_client.exists because it's not atomic with creation and introduce race condition
    try:
        blob_client.create_append_blob(if_unmodified_since=datetime(2000, 1, 1, tzinfo=timezone.utc))
    except ResourceModifiedError:
        pass
    blob_client.append_block(data=append_content)


@blob_error_handling_decorator
def upload_blob(blob_client: BlobClient, data: str, overwrite=True, lease=None):
    blob_client.upload_blob(data=data, overwrite=overwrite, lease=lease)


@blob_error_handling_decorator
def upload_file_to_blob(container_client: ContainerClient, file_path: str, blob_path: str):
    blob_client = container_client.get_blob_client(blob=blob_path)
    with open(file=file_path, mode="rb") as data:
        blob_client.upload_blob(data=data, overwrite=True)


@blob_error_handling_decorator
def download_blob_to_file(container_client: ContainerClient, blob_path: str, file_path: str):
    blob_client = container_client.get_blob_client(blob=blob_path)
    with open(file=file_path, mode="wb") as data:
        data.write(blob_client.download_blob().readall())


@blob_error_handling_decorator
def upload_dir_to_blob(container_client: ContainerClient, file_dir: str, blob_dir: str):
    """Upload a directory to a path inside the container"""
    """
    For flexbility, the destination path will not contains the basename of file_dir
    For example, if file_dir is /tmp/test_dir and blob_dir is /test,
      the content of /tmp/test_dir will be uploaded to /test
    The file /tmp/test_dir/test.txt will be uploaded to /test/test.txt
    """
    prefix = "" if blob_dir == "" else blob_dir + "/"
    for root, _, files in os.walk(file_dir):
        for name in files:
            dir_part = os.path.relpath(root, file_dir)
            dir_part = "" if dir_part == "." else dir_part + "/"
            file_path = os.path.join(root, name)
            blob_path = prefix + dir_part + name
            upload_file_to_blob(container_client=container_client, file_path=file_path, blob_path=blob_path)


@blob_error_handling_decorator
def download_blob_to_dir(container_client: ContainerClient, blob_dir: str, file_dir: str):
    """Download a path inside the container to a directory"""
    Path(file_dir).mkdir(parents=True, exist_ok=True)
    for blob in container_client.list_blobs(name_starts_with=blob_dir):
        blob_path = blob.name
        file_path = Path(file_dir) / Path(blob_path).name
        download_blob_to_file(container_client=container_client, blob_path=blob_path, file_path=file_path)


def init_azure_blob_service_client(storage_account_name, blob_container_name, credential) -> ContainerClient:
    """Initialize blob service client"""
    cloud = _get_cloud(cloud=_get_default_cloud_name())
    storage_endpoint = cloud.get(EndpointURLS.STORAGE_ENDPOINT, "core.windows.net")
    blob_url = f"https://{storage_account_name}.blob.{storage_endpoint}"
    blob_service_client = BlobServiceClient(blob_url, credential=credential)

    try:
        container = blob_service_client.get_container_client(blob_container_name)
        logger.info("Initialized blob service client.")
        if blob_service_client._client and blob_service_client._client._config:
            logger.info(f"Blob service client has api version: {blob_service_client._client._config.version}")
        return container
    except ClientAuthenticationError as e:
        msg = str(e)
        auth_error_msg = (
            "Failed to perform azure blob operation due to no available identity, please authenticate "
            f"the compute with proper identity. Original error: {msg}"
        )
        logger.error(auth_error_msg)
        raise StorageAuthenticationError(
            message=auth_error_msg,
            target=ErrorTarget.AZURE_RUN_STORAGE,
        ) from e
    except HttpResponseError as e:
        msg = str(e)
        if e.status_code == 403:
            auth_error_msg = (
                "Failed to perform azure blob operation due to invalid authentication, please assign RBAC role "
                f"'Storage Blob Data Contributor' to the service principal or client. Original error: {msg}"
            )
            logger.error(auth_error_msg)
            raise StorageAuthenticationError(
                message=auth_error_msg,
                target=ErrorTarget.AZURE_RUN_STORAGE,
            ) from e

        logger.error(f"Failed to perform azure blob operation due to invalid authentication. Original error: {msg}")
        raise


def serialize_intermedia_data(run_info: Union[FlowRunInfo, RunInfo], folder_path: Path):
    if run_info.inputs:
        run_info.inputs = persist_multimedia_data(run_info.inputs, folder_path)
    if run_info.output:
        output_data = persist_multimedia_data(run_info.output, folder_path)
        run_info.output = output_data
        if run_info.result:
            run_info.result = output_data
    if run_info.api_calls:
        run_info.api_calls = persist_multimedia_data(run_info.api_calls, folder_path)


class AzureMLRunStorageV2(AbstractRunStorage):
    FLOW_ARTIFACTS_FOLDER_NAME = "flow_artifacts"
    NODE_ARTIFACTS_FOLDER_NAME = "node_artifacts"
    FLOW_OUTPUTS_FOLDER_NAME = "flow_outputs"
    # instance_results.jsonl contains the inputs and outputs of all lines
    FLOW_INSTANCE_RESULTS_FILE_NAME = "instance_results.jsonl"
    META_FILE_NAME = "meta.json"
    DEFAULT_BATCH_SIZE = 25
    LINE_NUMBER_WIDTH = 9
    FLOW_OUTPUTS_ASSET_NAME = "flow_outputs"
    DEBUG_INFO_ASSET_NAME = "debug_info"
    TMP_DIR = ".tmp_dir"

    FLOW_RUN_INFO_PROPERTIES_TO_UPDATE = AbstractRunStorage.FLOW_RUN_INFO_PROPERTIES_TO_UPDATE

    def __init__(
        self,
        azure_storage_setting: AzureStorageSetting,
        mlflow_tracking_uri: str,
        asset_client: AssetClient,
        artifact_client: ArtifactClient,
        output_dir: Path,
    ) -> None:
        super().__init__(edition=PromptflowEdition.ENTERPRISE)
        self.flow_artifacts_root_path = azure_storage_setting.flow_artifacts_root_path.strip("/")
        self.output_datastore_name = azure_storage_setting.output_datastore_name
        self._mlflow_helper = MlflowHelper(mlflow_tracking_uri=mlflow_tracking_uri)
        self._asset_client = asset_client
        self._artifact_client = artifact_client
        self._persisted_runs = set()
        self._batch_size = self.DEFAULT_BATCH_SIZE
        self._output_dir = output_dir

        if not azure_storage_setting.blob_container_sas_token:
            # For the scenario where no credential is provided in datastore (e.g. Office team's workspace),
            # runtime does not receive sas token and need to use DefaultAzureCredential to authenticate
            logger.info("No sas token is provided, using DefaultAzureCredential to authenticate Blob access.")
            credential = get_default_credential()
        else:
            credential = azure_storage_setting.blob_container_sas_token

        self.blob_container_client = init_azure_blob_service_client(
            storage_account_name=azure_storage_setting.storage_account_name,
            blob_container_name=azure_storage_setting.blob_container_name,
            credential=credential,
        )
        self._write_flow_artifacts_meta_to_blob()

    def persist_node_run(self, run_info: RunInfo):
        """Persist node run record to remote storage"""
        with Timer(flow_logger, "Persist node info for run " + run_info.run_id):
            """Upload intermediate data"""
            tmp_output_path = (
                Path(os.getcwd()) / self.TMP_DIR / self.NODE_ARTIFACTS_FOLDER_NAME / str(run_info.index) / run_info.node
            )
            tmp_output_path.mkdir(parents=True, exist_ok=True)
            serialize_intermedia_data(run_info, tmp_output_path)
            upload_dir_to_blob(
                container_client=self.blob_container_client,
                file_dir=tmp_output_path,
                blob_dir=f"{self.flow_artifacts_root_path}/{self.NODE_ARTIFACTS_FOLDER_NAME}/{run_info.node}",
            )
            shutil.rmtree(tmp_output_path, ignore_errors=True)

            """Upload jsonl file"""
            node_record = NodeRunRecord.from_run_info(run_info)
            # For reduce nodes, the 'line_number' is None, we store the info in the 000000000.jsonl file
            # It's a storage contract with PromptflowService
            file_name = f"{str(node_record.line_number or 0).zfill(self.LINE_NUMBER_WIDTH)}.jsonl"
            blob_path = (
                f"{self.flow_artifacts_root_path}/{self.NODE_ARTIFACTS_FOLDER_NAME}/"
                f"{node_record.node_name}/{file_name}"
            )
            blob_client = self.blob_container_client.get_blob_client(blob=blob_path)
            upload_blob(blob_client=blob_client, data=node_record.serialize(), overwrite=True)

    def persist_flow_run(self, run_info: FlowRunInfo):
        """Persist flow run record to remote storage"""
        if not Status.is_terminated(run_info.status):
            return

        if self._is_root_run(run_info):
            logger.warning("The run info is a root flow run and should not invoke by persist_flow_run. Skip update it")
        else:
            with Timer(flow_logger, "Persist flow run info for run " + run_info.run_id):
                """Upload intermediate data"""
                tmp_output_path = (
                    Path(os.getcwd()) / self.TMP_DIR / str(run_info.index) / self.FLOW_ARTIFACTS_FOLDER_NAME
                )
                tmp_output_path.mkdir(parents=True, exist_ok=True)
                serialize_intermedia_data(run_info, tmp_output_path)
                upload_dir_to_blob(
                    container_client=self.blob_container_client,
                    file_dir=tmp_output_path,
                    blob_dir=f"{self.flow_artifacts_root_path}/{self.FLOW_ARTIFACTS_FOLDER_NAME}",
                )
                shutil.rmtree(tmp_output_path, ignore_errors=True)

                """Append jsonl file"""
                lower_bound = int(run_info.index) // self._batch_size * self._batch_size
                upper_bound = lower_bound + self._batch_size - 1
                file_name = (
                    f"{str(lower_bound).zfill(self.LINE_NUMBER_WIDTH)}_"
                    f"{str(upper_bound).zfill(self.LINE_NUMBER_WIDTH)}.jsonl"
                )
                blob_path = f"{self.flow_artifacts_root_path}/{self.FLOW_ARTIFACTS_FOLDER_NAME}/{file_name}"
                blob_client = self.blob_container_client.get_blob_client(blob=blob_path)
                self._append_line_run_record(run_info=run_info, blob_client=blob_client)

                """Append instance_results.jsonl"""
                self._persist_to_instance_results(run_info=run_info)

    def _append_line_run_record(self, run_info: FlowRunInfo, blob_client: BlobClient):
        line_record = LineRunRecord.from_run_info(run_info)
        try:
            append_blob(blob_client, line_record.serialize() + "\n")
        except HttpResponseError as e:
            msg = str(e)
            if e.status_code == 413:
                if line_record.run_info and ("api_calls" in line_record.run_info):
                    line_record.run_info.pop("api_calls")
                    size_error_msg = (
                        "Failed to append blob operation due to large data size. "
                        f"Will drop the trace info and try to upload again. Original error: {msg}"
                    )
                    logger.error(size_error_msg)
                    return append_blob(blob_client, line_record.serialize() + "\n")
            raise

    def _serialize_intermedia_data(self, run_info: Union[FlowRunInfo, RunInfo], folder_path: Path):
        if run_info.inputs:
            run_info.inputs = persist_multimedia_data(run_info.inputs, folder_path)
        if run_info.output:
            output_data = persist_multimedia_data(run_info.output, folder_path)
            run_info.output = output_data
            # This is a backward compatibility code for old contract version with result field
            if hasattr(run_info, "result"):
                run_info.result = output_data
        if run_info.api_calls:
            run_info.api_calls = persist_multimedia_data(run_info.api_calls, folder_path)

    def update_flow_run_info(self, run_info: FlowRunInfo):
        """Update the following flow run info fields: status, end_time, run_info"""
        if not Status.is_terminated(run_info.status):
            return

        if self._is_root_run(run_info):
            return self.register_root_run_artifacts(run_info.root_run_id, run_info.status)
        else:
            logger.warning("The run info is not a root flow run and should not invoke by update_root_flow_run_info.")

    def register_root_run_artifacts(self, run_id: str, status: Status):
        if not Status.is_terminated(status):
            return

        debug_info_asset_id = self._create_debug_info_asset(run_id)
        output_asset_infos = {self.DEBUG_INFO_ASSET_NAME: OutputAssetInfo(debug_info_asset_id)}

        # In all terminated status, we should create outputs asset and instance results artifact for resume.
        flow_output_asset_id = self._create_flow_output_asset(run_id)
        output_asset_infos[self.FLOW_OUTPUTS_ASSET_NAME] = OutputAssetInfo(flow_output_asset_id)

        try:
            # Swallow create instance results exception, because it's not critical for BatchRun.
            self._create_instance_results_artifact(run_id)
        except Exception as e:
            logger.warning(f"Failed to create instance_results artifact due to error: {str(e)}.")

        return output_asset_infos

    def persist_status_summary(self, metrics: dict, flow_run_id: str):
        # Executor code invoke storage.persist_status_summary. So we should keep this method in storage
        self._mlflow_helper.persist_status_summary(metrics=metrics, flow_run_id=flow_run_id)

    def _create_debug_info_asset(self, root_run_id: str):
        asset_id = self._asset_client.create_unregistered_output(
            run_id=root_run_id,
            datastore_name=self.output_datastore_name,
            relative_path=self.flow_artifacts_root_path,
            output_name=self.DEBUG_INFO_ASSET_NAME,
        )
        logger.info(f"Created {self.DEBUG_INFO_ASSET_NAME} Asset: {asset_id}")
        return asset_id

    def _create_flow_output_asset(self, root_run_id: str):
        output_blob_folder_path = f"{self.flow_artifacts_root_path}/{self.FLOW_OUTPUTS_FOLDER_NAME}"
        upload_dir_to_blob(self.blob_container_client, self._output_dir.absolute(), output_blob_folder_path)
        asset_id = self._asset_client.create_unregistered_output(
            run_id=root_run_id,
            datastore_name=self.output_datastore_name,
            relative_path=output_blob_folder_path,
            output_name=self.FLOW_OUTPUTS_ASSET_NAME,
        )
        logger.info(f"Created {self.FLOW_OUTPUTS_ASSET_NAME} output Asset: {asset_id}")
        return asset_id

    def _persist_to_instance_results(self, run_info: FlowRunInfo):
        output_blob_file_name = f"{self.flow_artifacts_root_path}/{self.FLOW_INSTANCE_RESULTS_FILE_NAME}"
        output_blob_client = self.blob_container_client.get_blob_client(blob=output_blob_file_name)
        output_json_lines = self._serialize_instance_results(run_info=run_info)
        append_blob(output_blob_client, output_json_lines + "\n")

    def _create_instance_results_artifact(self, run_id: str):
        output_blob_file_name = f"{self.flow_artifacts_root_path}/{self.FLOW_INSTANCE_RESULTS_FILE_NAME}"
        try:
            self._artifact_client.register_artifact(
                run_id=run_id,
                datastore_name=self.output_datastore_name,
                relative_path=output_blob_file_name,
                path=self.FLOW_INSTANCE_RESULTS_FILE_NAME,
            )
            logger.info(f"Created {self.FLOW_INSTANCE_RESULTS_FILE_NAME} Artifact.")
        except UserAuthenticationError as e:
            logger.warning(
                "Skip creating instance_results artifact due to authentication "
                f"error: {str(e)}. Please grant the compute with "
                "artifact write permission if you need it to be created."
            )

    def _write_flow_artifacts_meta_to_blob(self):
        blob_path = f"{self.flow_artifacts_root_path}/{self.META_FILE_NAME}"
        blob_client = self.blob_container_client.get_blob_client(blob=blob_path)
        meta = {"batch_size": self._batch_size}
        upload_blob(blob_client, json.dumps(meta), overwrite=True)

    def get_flow_run(self, run_id: str, flow_id=None) -> FlowRunInfo:
        return None

    def get_relative_path_in_blob(self, blob_client) -> str:
        """Get a json string that indicates the container and relative path in remote blob"""
        blob_path_info = {
            "container": blob_client.container_name,
            "relative_path": blob_client.blob_name,
        }
        return json.dumps(blob_path_info)

    def _is_root_run(self, run_info: FlowRunInfo) -> bool:
        return run_info.run_id == run_info.root_run_id

    def _serialize_instance_results(self, run_info: FlowRunInfo) -> str:
        result = {
            LINE_NUMBER_KEY: run_info.index,
            STATUS_KEY: run_info.status.value,
        }

        if run_info.inputs is not None:
            for k, v in run_info.inputs.items():
                result.update({f"inputs.{k}": v})

        if run_info.output is not None:
            for k, v in run_info.output.items():
                result.update({f"{k}": v})

        return json.dumps(result)
