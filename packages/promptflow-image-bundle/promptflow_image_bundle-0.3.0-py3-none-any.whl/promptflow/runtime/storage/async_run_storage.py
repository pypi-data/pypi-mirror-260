# ----------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
# ----------------------------------------------------------
import contextlib
import copy
import json
import shutil
import uuid
from pathlib import Path
from tempfile import gettempdir
from typing import Any, Dict, List, Optional

from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobClient, BlobLeaseClient

from promptflow._internal import ErrorResponse, persist_multimedia_data, serialize
from promptflow.contracts.run_info import FlowRunInfo, RunInfo, Status
from promptflow.runtime._errors import DataInputsNotfound, MissingDeploymentConfigs
from promptflow.runtime.contracts.azure_storage_setting import AzureStorageSetting
from promptflow.runtime.data import prepare_data
from promptflow.runtime.runtime_config import DeploymentConfig
from promptflow.runtime.storage.azureml_run_storage_v2 import (
    blob_error_handling_decorator,
    init_azure_blob_service_client,
    serialize_intermedia_data,
    upload_blob,
    upload_dir_to_blob,
)
from promptflow.runtime.utils import logger
from promptflow.runtime.utils._utils import get_default_credential
from promptflow.runtime.utils.downloader import _get_last_part_of_uri
from promptflow.runtime.utils.multimedia_data_converter import (
    convert_path_to_url,
    convert_path_to_url_for_run_info,
    convert_url_to_path,
)
from promptflow.runtime.utils.retry_utils import retry
from promptflow.storage import AbstractRunStorage


@contextlib.contextmanager
def acquire_blob_lease(blob_client: BlobClient, lease_duration: int = 15) -> Optional[BlobLeaseClient]:
    lease_client = None
    try:
        if blob_client.exists():
            lease_client = acquire_lease_with_retry(blob_client, lease_duration)
        yield lease_client
    finally:
        if lease_client is not None:
            try:
                lease_client.release()
            except Exception:
                pass


@retry(ResourceExistsError, tries=10)
def acquire_lease_with_retry(blob_client: BlobClient, lease_duration: int = 15) -> BlobLeaseClient:
    """Handle ResourceExistsError of LeaseAlreadyPresent error code with retry in conflict case."""
    return blob_client.acquire_lease(lease_duration=lease_duration)


class AsyncRunStorage(AbstractRunStorage):
    FLOW_STATUS = "flow_status"
    NODE_STATUS = "status"
    FLOW_INFO_PATH = "flow_info_path"
    FLOW_TRACE_PATH = "flow_trace_path"
    FLOW_OUTPUT_PATH = "flow_output_path"
    SYSTEM_METRICS = "system_metrics"
    ERROR_RESPONSE = "error_response"
    NODE_INFO_PATH = "node_info_path"
    NODE_OUTPUT_PATH = "node_output_path"
    NODES = "nodes"
    SINGLE_NODE_RUNS = "single_node_runs"
    NODE_INFOS = "node_infos"
    NODE_OUTPUTS = "node_outputs"
    FLOW_RUNS = "flow_runs"
    NODE_RUNS = "node_runs"

    def __init__(
        self,
        run_id: str,
        azure_storage_setting: AzureStorageSetting,
        is_default_variant: bool = True,
        node_variant_id: Optional[str] = None,
        deployment_config: DeploymentConfig = None,
        flow_yaml_path: Path = None,
    ):
        self._run_id = run_id
        self._is_default_variant = is_default_variant
        self._node_variant_id = node_variant_id
        self._output_datastore_name = azure_storage_setting.output_datastore_name
        self._flow_artifacts_root_path = azure_storage_setting.flow_artifacts_root_path

        # deployment_config is needed when generate blob universal link in overview.json
        self._deployment_config = deployment_config
        self._flow_yaml_path = flow_yaml_path

        if not azure_storage_setting.blob_container_sas_token:
            logger.info("No sas token is provided, using DefaultAzureCredential to authenticate Blob access.")
            credential = get_default_credential()
        else:
            credential = azure_storage_setting.blob_container_sas_token

        self._container_client = init_azure_blob_service_client(
            storage_account_name=azure_storage_setting.storage_account_name,
            blob_container_name=azure_storage_setting.blob_container_name,
            credential=credential,
        )

    def persist_node_run(self, run_info: RunInfo):
        """Persist node run record to blob storage"""
        # serialize node output to local folder
        tmp_node_outputs_dir = Path(gettempdir()) / str(uuid.uuid4())
        tmp_node_outputs_dir.mkdir(parents=True, exist_ok=True)
        node_output_data = persist_multimedia_data(run_info.output, tmp_node_outputs_dir)

        node_outputs_blob_folder = f"{self.NODE_OUTPUTS}/{run_info.node}"
        if self._node_variant_id is not None:
            # use different folder for each node variant
            node_outputs_blob_folder = f"{node_outputs_blob_folder}{self._node_variant_id}"

        node_output_data = convert_path_to_url(
            self._flow_yaml_path, node_output_data, f"{self._get_base_blob_universal_link()}/{node_outputs_blob_folder}"
        )
        node_output_file = tmp_node_outputs_dir / f"{run_info.node}.json"
        with open(node_output_file, "w") as f:
            json.dump(serialize(node_output_data), f)

        # upload node outputs to blob storage
        node_outputs_blob_path = f"{self._flow_artifacts_root_path}/{node_outputs_blob_folder}"
        upload_dir_to_blob(
            container_client=self._container_client,
            file_dir=tmp_node_outputs_dir,
            blob_dir=node_outputs_blob_path,
        )
        shutil.rmtree(tmp_node_outputs_dir, ignore_errors=True)

        # serialize node infos to local folder
        tmp_node_infos_dir = Path(gettempdir()) / str(uuid.uuid4())
        tmp_node_infos_dir.mkdir(parents=True, exist_ok=True)
        # redact node output and result content from run info
        run_info.output = None
        run_info.result = None
        serialize_intermedia_data(run_info, tmp_node_infos_dir)

        node_infos_blob_folder = f"{self.NODE_INFOS}/{run_info.node}"
        if self._node_variant_id is not None:
            # use different folder for each node variant
            node_infos_blob_folder = f"{node_infos_blob_folder}{self._node_variant_id}"

        convert_path_to_url_for_run_info(
            self._flow_yaml_path, run_info, f"{self._get_base_blob_universal_link()}/{node_infos_blob_folder}"
        )
        node_info_file = tmp_node_infos_dir / f"{run_info.node}.json"
        serialized_run_info = serialize(run_info)
        with open(node_info_file, "w") as f:
            json.dump(serialized_run_info, f)
        # upload node infos to blob storage
        node_infos_blob_path = f"{self._flow_artifacts_root_path}/{node_infos_blob_folder}"
        upload_dir_to_blob(
            container_client=self._container_client,
            file_dir=tmp_node_infos_dir,
            blob_dir=node_infos_blob_path,
        )
        shutil.rmtree(tmp_node_infos_dir, ignore_errors=True)

        node_info_path = self._get_blob_universal_link(f"{node_infos_blob_folder}/{run_info.node}.json")
        node_output_path = self._get_blob_universal_link(f"{node_outputs_blob_folder}/{run_info.node}.json")
        error_response = None if run_info.error is None else ErrorResponse.from_error_dict(run_info.error).to_dict()
        self.set_overview_node_run_status(
            node_name=run_info.node,
            status=run_info.status.value,
            system_metrics=run_info.system_metrics,
            error_response=error_response,
            node_info_path=node_info_path,
            node_output_path=node_output_path,
        )

    def persist_flow_run(self, run_info: FlowRunInfo):
        """Persist flow run record to blob storage"""
        if not Status.is_terminated(run_info.status):
            return

        # serialize flow run info to local folder
        tmp_flow_info_dir = Path(gettempdir()) / str(uuid.uuid4())
        tmp_flow_info_dir.mkdir(parents=True, exist_ok=True)
        serialize_intermedia_data(run_info, tmp_flow_info_dir)
        convert_path_to_url_for_run_info(self._flow_yaml_path, run_info, self._get_base_blob_universal_link())

        flow_trace = run_info.api_calls
        flow_trace_file = tmp_flow_info_dir / "flow_trace.json"
        with open(flow_trace_file, "w") as f:
            json.dump(serialize(flow_trace), f)

        # redact trace inputs/outputs from flow run info
        redact_flow_info = copy.deepcopy(run_info)
        self._redact_trace(redact_flow_info.api_calls)
        # redact flow output and result content from flow run info
        redact_flow_info.output = None
        redact_flow_info.result = None
        flow_info_file = tmp_flow_info_dir / "flow_run_info.json"
        with open(flow_info_file, "w") as f:
            json.dump(serialize(redact_flow_info), f)

        flow_output = run_info.output
        flow_output_file = tmp_flow_info_dir / "flow_output.json"
        with open(flow_output_file, "w") as f:
            json.dump(serialize(flow_output), f)

        # upload flow run info to blob storage
        upload_dir_to_blob(
            container_client=self._container_client,
            file_dir=tmp_flow_info_dir,
            blob_dir=self._flow_artifacts_root_path,
        )
        shutil.rmtree(tmp_flow_info_dir, ignore_errors=True)

        flow_info_path = self._get_blob_universal_link("flow_run_info.json")
        flow_trace_path = self._get_blob_universal_link("flow_trace.json")
        flow_output_path = self._get_blob_universal_link("flow_output.json")
        error_response = None if run_info.error is None else ErrorResponse.from_error_dict(run_info.error).to_dict()
        self.set_overview_flow_run_status(
            status=run_info.status.value,
            error_response=error_response,
            flow_info_path=flow_info_path,
            flow_trace_path=flow_trace_path,
            flow_output_path=flow_output_path,
        )

    @blob_error_handling_decorator
    def update_aggregation_metrics(self, metrics: dict[str, Any]):
        """Update aggregation metrics to flow run info blob"""
        if not metrics:
            return
        flow_info_blob = f"{self._flow_artifacts_root_path}/flow_run_info.json"
        blob_client = self._container_client.get_blob_client(blob=flow_info_blob)
        if not blob_client.exists():
            # Should not happen since metrics are generated later.
            logger.warning(f"[{self._run_id}] Flow run info doesn't exist. Skip")
            return
        flow_info = json.loads(blob_client.download_blob().readall())
        flow_info["metrics"] = metrics
        upload_blob(blob_client, data=json.dumps(flow_info), overwrite=True)

    def download_dependency_nodes_outputs(self, dependency_nodes: dict[str, str], tmp_node_dir: Path) -> dict[str, Any]:
        """Use universal link to download dependency nodes outputs"""
        if not dependency_nodes:
            return dependency_nodes

        # download node outputs
        for node_name, universal_link in dependency_nodes.items():
            prepare_data(universal_link, tmp_node_dir)
            downloaded_file_name = _get_last_part_of_uri(universal_link)
            node_output_file = tmp_node_dir / downloaded_file_name
            if not node_output_file.is_file():
                raise DataInputsNotfound(message=f"Dependency node output file {universal_link} doesn't exist.")

            with open(node_output_file, "r") as f:
                node_output = json.load(f)
                node_output = convert_url_to_path(self._flow_yaml_path, node_output, tmp_node_dir)
                dependency_nodes[node_name] = node_output

        return dependency_nodes

    def start_flow_run(self):
        self.set_overview_flow_run_status(status=Status.Running.value)

    def cancel_flow_run(self):
        self.set_overview_flow_run_status(status=Status.Canceled.value)

    def fail_flow_run(self, error_response=None):
        self.set_overview_flow_run_status(status=Status.Failed.value, error_response=error_response)

    def get_flow_run_status(self) -> str:
        overview = self.get_overview()
        return overview.get(self.FLOW_STATUS)

    def start_node_run(self, node: str):
        self.set_overview_node_run_status(node_name=node, status=Status.Running.value)

    def cancel_node_run(self, node: str):
        self.set_overview_node_run_status(node_name=node, status=Status.Canceled.value)

    def fail_node_run(self, node: str, error_response=None):
        self.set_overview_node_run_status(node_name=node, status=Status.Failed.value, error_response=error_response)

    def get_node_run_status(self, node: str) -> str:
        overview = self.get_overview()
        if self._node_variant_id is None:
            node_info = overview.get(self.NODES, {}).get(node)
            if node_info is not None:
                return node_info.get(self.NODE_STATUS)
        else:
            node_variants = overview.get(self.SINGLE_NODE_RUNS, {}).get(node)
            if node_variants is not None:
                node_info = node_variants.get(self._node_variant_id)
                if node_info is not None:
                    return node_info.get(self.NODE_STATUS)

    def cancelling_run(self) -> bool:
        cancel_requested = False
        overview = self.get_overview()
        # Cancel request doesn't differentiate flow test or single node run currently, so check both cases here.
        flow_status = overview.get(self.FLOW_STATUS)
        if flow_status is not None and not Status.is_terminated(flow_status):
            self.set_overview_flow_run_status(status=Status.CancelRequested.value)
            cancel_requested = True
            logger.info(f"[{self._run_id}] Set async run flow status to {Status.CancelRequested.value}.")
        else:
            self.set_overview_node_run_status_to_cancel_requested()
            cancel_requested = True
            logger.info(f"[{self._run_id}] Set async run node status to {Status.CancelRequested.value}.")

        return cancel_requested

    def set_overview_flow_run_status(
        self,
        status: str,
        error_response=None,
        flow_info_path=None,
        flow_trace_path=None,
        flow_output_path=None,
    ):
        # overview blob may be updated by multiple processes,
        # so we may need to acquire a lease before updating it.
        with acquire_blob_lease(self._get_overview_blob()) as lease:
            overview = self.get_overview()
            overview[self.FLOW_STATUS] = status
            overview[self.ERROR_RESPONSE] = error_response
            overview[self.FLOW_INFO_PATH] = flow_info_path
            overview[self.FLOW_TRACE_PATH] = flow_trace_path
            overview[self.FLOW_OUTPUT_PATH] = flow_output_path

            self._upload_overview(overview, lease)

    def set_overview_node_run_status(
        self,
        node_name: str,
        status: str,
        system_metrics=None,
        error_response=None,
        node_info_path=None,
        node_output_path=None,
    ):
        # overview blob may be updated concurrently, so we need to acquire a lease before modifying it.
        with acquire_blob_lease(self._get_overview_blob()) as lease:
            overview = self.get_overview()

            if self._is_default_variant:
                # update "nodes" if default variant
                if overview.get(self.NODES) is None:
                    overview[self.NODES] = {}

                node_info = overview[self.NODES].get(node_name)
                if node_info is None:
                    node_info = {}
                node_info[self.NODE_STATUS] = status
                node_info[self.SYSTEM_METRICS] = system_metrics
                node_info[self.ERROR_RESPONSE] = error_response
                node_info[self.NODE_INFO_PATH] = node_info_path
                node_info[self.NODE_OUTPUT_PATH] = node_output_path
                overview[self.NODES].update({node_name: node_info})

            if self._node_variant_id is not None:
                # update "single_node_runs" if has variant id
                if overview.get(self.SINGLE_NODE_RUNS) is None:
                    overview[self.SINGLE_NODE_RUNS] = {}

                single_node_run = overview[self.SINGLE_NODE_RUNS].get(node_name)
                if single_node_run is None:
                    single_node_run = {}

                variant_node_info = {
                    self.NODE_STATUS: status,
                    self.SYSTEM_METRICS: system_metrics,
                    self.ERROR_RESPONSE: error_response,
                    self.NODE_INFO_PATH: node_info_path,
                    self.NODE_OUTPUT_PATH: node_output_path,
                }
                single_node_run.update({self._node_variant_id: variant_node_info})
                overview[self.SINGLE_NODE_RUNS].update({node_name: single_node_run})

            self._upload_overview(overview, lease)

    def set_overview_node_run_status_to_cancel_requested(self):
        with acquire_blob_lease(self._get_overview_blob()) as lease:
            overview = self.get_overview()

            for node_name, node_info in overview.get(self.NODES, {}).items():
                if not Status.is_terminated(node_info.get(self.NODE_STATUS)):
                    node_info[self.NODE_STATUS] = Status.CancelRequested.value
                    node_info[self.SYSTEM_METRICS] = None
                    node_info[self.ERROR_RESPONSE] = None
                    node_info[self.NODE_INFO_PATH] = None
                    node_info[self.NODE_OUTPUT_PATH] = None
                    overview[self.NODES].update({node_name: node_info})

            for node_name, node_variant in overview.get(self.SINGLE_NODE_RUNS, {}).items():
                for variant_id, node_info in node_variant.items():
                    if not Status.is_terminated(node_info.get(self.NODE_STATUS)):
                        variant_node_info = {
                            self.NODE_STATUS: Status.CancelRequested.value,
                            self.SYSTEM_METRICS: None,
                            self.ERROR_RESPONSE: None,
                            self.NODE_INFO_PATH: None,
                            self.NODE_OUTPUT_PATH: None,
                        }
                        node_variant.update({variant_id: variant_node_info})
                        overview[self.SINGLE_NODE_RUNS].update({node_name: node_variant})

            self._upload_overview(overview, lease)

    def get_overview(self) -> dict:
        blob_client = self._get_overview_blob()
        if blob_client.exists():
            overview = json.loads(blob_client.download_blob().readall())
        else:
            overview = {}
        return overview

    def _upload_overview(self, overview: dict, lease=None):
        blob_client = self._get_overview_blob()
        upload_blob(blob_client, data=json.dumps(overview), overwrite=True, lease=lease)

    def _get_overview_blob(self) -> BlobClient:
        overview_blob_path = f"{self._flow_artifacts_root_path}/overview.json"
        return self._container_client.get_blob_client(blob=overview_blob_path)

    def _redact_trace(self, trace_info: Optional[List[Dict[str, Any]]] = None):
        if trace_info is None:
            return
        for trace in trace_info:
            trace["inputs"] = None
            trace["output"] = None
            if trace["children"] is not None:
                self._redact_trace(trace["children"])

    def _get_blob_universal_link(self, path: str):
        base_blob_universal_link = self._get_base_blob_universal_link()
        return f"{base_blob_universal_link}/{path}"

    def _get_base_blob_universal_link(self):
        if self._deployment_config is None:
            raise MissingDeploymentConfigs(message=f"deployment config is not set for run {self._run_id}.")

        from azure.ai.ml.constants._common import LONG_URI_FORMAT

        base_blob_universal_link = LONG_URI_FORMAT.format(
            self._deployment_config.subscription_id,
            self._deployment_config.resource_group,
            self._deployment_config.workspace_name,
            self._output_datastore_name,
            f"{self._flow_artifacts_root_path}",
        )
        return base_blob_universal_link
