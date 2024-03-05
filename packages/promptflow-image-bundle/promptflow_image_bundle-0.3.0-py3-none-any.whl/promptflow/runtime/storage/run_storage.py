import json
import logging
import os
from dataclasses import _MISSING_TYPE
from datetime import datetime, timedelta
from pathlib import Path
from types import GeneratorType
from typing import Optional

from promptflow._internal import deserialize_dataclass, serialize
from promptflow.contracts.run_info import FlowRunInfo, RunInfo
from promptflow.exceptions import ErrorTarget
from promptflow.runtime._errors import RunInfoNotFoundInStorageError
from promptflow.runtime.constants import STORAGE_ACCOUNT_NAME, AzureMLConfig, PromptflowEdition
from promptflow.runtime.contracts.azure_storage_mode import AzureStorageMode
from promptflow.runtime.contracts.azure_storage_setting import AzureStorageSetting
from promptflow.runtime.utils._utils import get_mlflow_tracking_uri


class AbstractRunStorage:
    FLOW_RUN_INFO_PROPERTIES_TO_UPDATE = {
        "start_time",
        "end_time",
        "run_info",
        "status",
        "root_run_id",
        "parent_run_id",
    }

    def __init__(self, edition=PromptflowEdition.COMMUNITY):
        self._edition = edition

    def persist_node_run(self, run_info: RunInfo):
        raise NotImplementedError("AbstractRunStorage is an abstract class, no implementation for persist_node_run.")

    def persist_flow_run(self, run_info: FlowRunInfo):
        raise NotImplementedError("AbstractRunStorage is an abstract class, no implementation for persist_flow_run.")

    def update_flow_run_info(self, run_info: FlowRunInfo):
        msg = "AbstractRunStorage is an abstract class, no implementation for update_flow_run_info."
        raise NotImplementedError(msg)

    def get_node_run(self, run_id: str) -> RunInfo:
        raise NotImplementedError("AbstractRunStorage is an abstract class, no implementation for get_node_run.")

    def get_flow_run(self, run_id: str, flow_id=None) -> FlowRunInfo:
        raise NotImplementedError("AbstractRunStorage is an abstract class, no implementation for get_flow_run.")

    def _start_aml_root_run(self, run_id: str) -> None:
        raise NotImplementedError(
            "Failed to start a run in workspace, this should only be called with enterprise edition of promptflow sdk."
        )

    def _end_aml_bulk_test_run(self, bulk_test_id: str, bulk_test_status: str):
        raise NotImplementedError(
            "Failed to end a bulk test run in workspace, "
            "this should only be called with enterprise edition of promptflow sdk."
        )

    def cancel_run(self, run_id: str):
        raise NotImplementedError("Failed to cancel a run due to no implementation.")

    def cancel_flow_child_runs(self, flow_id: str, run_id: str):
        raise NotImplementedError(
            "AbstractRunStorage is an abstract class, no implementation for cancel_flow_child_runs."
        )

    def get_run_status(self, run_id: str):
        raise NotImplementedError("Failed to get run status due to no implementation..")

    def persist_status_summary(self, metrics: dict, flow_run_id: str):
        raise NotImplementedError("Failed to persist status summary due to no implementation.")

    @staticmethod
    def init_from_env() -> "AbstractRunStorage":
        if os.environ.get("PROMPTFLOW_AZURE_STORAGE_MODE", None) == AzureStorageMode.Blob.name:
            from promptflow.runtime.storage.azureml_run_storage_v2 import AzureMLRunStorageV2
            from promptflow.runtime.utils._artifact_client import ArtifactClient
            from promptflow.runtime.utils._asset_client import AssetClient
            from promptflow.runtime.utils._utils import get_default_credential

            subscription_id = os.environ.get(AzureMLConfig.SUBSCRIPTION_ID, None)
            resource_group_name = os.environ.get(AzureMLConfig.RESOURCE_GROUP_NAME, None)
            workspace_name = os.environ.get(AzureMLConfig.WORKSPACE_NAME, None)
            mt_endpoint = os.environ.get(AzureMLConfig.MT_ENDPOINT, None)

            mlflow_tracking_uri = get_mlflow_tracking_uri(
                subscription_id=subscription_id,
                resource_group_name=resource_group_name,
                workspace_name=workspace_name,
                mt_endpoint=mt_endpoint,
            )

            credential = get_default_credential()
            storage_account_name = (os.environ.get(STORAGE_ACCOUNT_NAME, None),)
            if isinstance(storage_account_name, tuple):
                storage_account_name = storage_account_name[0]

            azure_storage_setting = AbstractRunStorage.init_azure_storage_setting(
                subscription_id, resource_group_name, storage_account_name, credential
            )
            asset_client = AssetClient(
                subscription_id=subscription_id,
                resource_group=resource_group_name,
                workspace_name=workspace_name,
                service_endpoint=mt_endpoint,
                credential=credential,
            )
            artifact_client = ArtifactClient(
                subscription_id=subscription_id,
                resource_group=resource_group_name,
                workspace_name=workspace_name,
                service_endpoint=mt_endpoint,
                credential=credential,
            )
            return AzureMLRunStorageV2(
                azure_storage_setting=azure_storage_setting,
                mlflow_tracking_uri=mlflow_tracking_uri,
                asset_client=asset_client,
                artifact_client=artifact_client,
                output_dir=Path(os.getcwd()) / ".output_dir",  # only for test
            )
        else:
            logging.info("Init DummyRunStorage.")
            return DummyRunStorage()

    @staticmethod
    def init_dummy() -> "AbstractRunStorage":
        return DummyRunStorage()

    @staticmethod
    def init_azure_storage_setting(
        subscription_id: str,
        resource_group_name: str,
        storage_account_name: str,
        credential,
        default_run_id: Optional[str] = None,
    ) -> AzureStorageSetting:
        from azure.mgmt.storage import StorageManagementClient
        from azure.storage.blob import generate_container_sas

        container_name = "flow-artifacts"
        # Have to get account_key by StorageManagementClient, default_credential does not contain it
        storage_client = StorageManagementClient(credential, subscription_id)
        keys = storage_client.storage_accounts.list_keys(resource_group_name, storage_account_name)
        account_key = keys.keys[0].value
        bulk_run_id = os.environ.get("PROMPTFLOW_BULK_RUN_ID", default_run_id)
        sas_token = generate_container_sas(
            storage_account_name,
            container_name,
            account_key=account_key,
            permission="racwdl",
            expiry=datetime.utcnow() + timedelta(days=1),  # expiry time
        )
        return AzureStorageSetting(
            azure_storage_mode=AzureStorageMode.Blob,
            storage_account_name=storage_account_name,
            blob_container_name="flow-artifacts",
            flow_artifacts_root_path=f"promptflow/PromptFlowArtifacts/{bulk_run_id}",
            blob_container_sas_token=sas_token,
            output_datastore_name="workspaceblobstore",
        )


class DummyRunStorage(AbstractRunStorage):
    def __init__(self):
        self.dummy_run_dir: Path = os.environ.get("PROMPTFLOW_DUMMY_RUN_DIR")
        if self.dummy_run_dir:
            self.dummy_run_dir = Path(self.dummy_run_dir)
            self.dummy_run_dir.mkdir(parents=True, exist_ok=True)
        super().__init__(edition=PromptflowEdition.COMMUNITY)

    def persist_node_run(self, run_info: RunInfo):
        if not self.dummy_run_dir:
            #  Do nothing if dummy_run_dir is not set
            return
        run_file = self.dummy_run_dir / f"{run_info.run_id}.json"
        data = serialize(run_info)
        with open(run_file, "w") as fout:
            json.dump(data, fout, indent=2)
        print(f"NodeRun {run_info.run_id} written to {run_file}")

    def persist_flow_run(self, run_info: FlowRunInfo):
        if run_info.output and self._have_generator_output(run_info.output):
            return

        if not self.dummy_run_dir:
            #  Do nothing if dummy_run_dir is not set
            return
        run_file = self.dummy_run_dir / f"{run_info.run_id}.json"
        data = serialize(run_info)
        with open(run_file, "w") as fout:
            json.dump(data, fout, indent=2)
        print(f"FlowRun {run_info.run_id} written to {run_file}")

    def get_flow_run(self, run_id: str, flow_id=None) -> Optional[FlowRunInfo]:
        if not self.dummy_run_dir:
            raise RunInfoNotFoundInStorageError(
                "DummyRunStorage doesn't have a directory initialized.",
                target=ErrorTarget.RUN_STORAGE,
                storage_type=type(self),
            )
        run_file = self.dummy_run_dir / f"{run_id}.json"
        if not run_file.exists():
            raise RunInfoNotFoundInStorageError(
                f"Run file {run_file} not found.", target=ErrorTarget.RUN_STORAGE, storage_type=type(self)
            )
        with open(run_file, "r") as fin:
            data = json.load(fin)
            return deserialize_flow_run_info(data)

    def update_flow_run_info(self, run_info: FlowRunInfo):
        self.persist_flow_run(run_info)

    def get_node_run(self, run_id: str) -> Optional[RunInfo]:
        if not self.dummy_run_dir:
            raise RunInfoNotFoundInStorageError(
                "DummyRunStorage doesn't have a directory initialized.",
                target=ErrorTarget.RUN_STORAGE,
                storage_type=type(self),
            )
        run_file = self.dummy_run_dir / f"{run_id}.json"
        if not run_file.exists():
            raise RunInfoNotFoundInStorageError(
                f"Run file {run_file} not found.", target=ErrorTarget.RUN_STORAGE, storage_type=type(self)
            )
        with open(run_file, "r") as fin:
            data = json.load(fin)
            return deserialize_node_run_info(data)

    def persist_status_summary(self, metrics: dict, flow_run_id: str):
        if not self.dummy_run_dir:
            #  Do nothing if dummy_run_dir is not set
            return
        metrics_file = self.dummy_run_dir / f"{flow_run_id}_inner_metrics.json"
        data = serialize(metrics)
        with open(metrics_file, "w") as fout:
            json.dump(data, fout, indent=2)
        print(f"Metrics of NodeRun {flow_run_id} written to {metrics_file}.")

    def _have_generator_output(self, outputs: dict):
        for _, v in outputs.items():
            if isinstance(v, GeneratorType):
                return True
        return False


def deserialize_flow_run_info(data: dict):
    from promptflow.contracts.run_info import FlowRunInfo

    # Backward compatibility for old version of RunInfo which has result field
    value = deserialize_dataclass(FlowRunInfo, data)
    if isinstance(value.output, _MISSING_TYPE) and hasattr(value, "result"):
        value.output = value.result
    return value


def deserialize_node_run_info(data: dict):
    from promptflow.contracts.run_info import RunInfo

    value = deserialize_dataclass(RunInfo, data)
    # Backward compatibility for old version of RunInfo which has result field
    if isinstance(value.output, _MISSING_TYPE) and hasattr(value, "result"):
        value.output = value.result
    return value


class RuntimeAuthErrorType:
    WORKSPACE = "workspace"
    STORAGE = "storage"
