import json
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, Mapping, Optional, TypeVar, Union

from promptflow._internal import serialize
from promptflow.contracts.run_mode import RunMode
from promptflow.runtime.utils._contract_util import normalize_dict_keys_camel_to_snake

from ._errors import InvalidFlowSourceType
from .azure_storage_setting import AzureStorageSetting
from .predefined_policies import PredefinedPolicies

T = TypeVar("T")


@dataclass
class BatchDataInput:
    data_uri: str = None

    @staticmethod
    def deserialize(data: dict) -> "BatchDataInput":
        data = normalize_dict_keys_camel_to_snake(data)
        return BatchDataInput(
            data_uri=data.get("data_uri", ""),
        )


@dataclass
class CreatedBy:
    user_object_id: str = None
    user_tenant_id: str = None
    user_name: str = None

    @staticmethod
    def deserialize(data: dict) -> "CreatedBy":
        data = normalize_dict_keys_camel_to_snake(data)
        return CreatedBy(
            user_object_id=data.get("user_object_id", ""),
            user_tenant_id=data.get("user_tenant_id", ""),
            user_name=data.get("user_name", ""),
        )


@dataclass
class AzureFileShareInfo:
    working_dir: str
    sas_url: Optional[str] = None

    @staticmethod
    def deserialize(data: dict):
        return AzureFileShareInfo(working_dir=data.get("working_dir", ""), sas_url=data.get("sas_url", ""))


@dataclass
class SnapshotInfo:
    snapshot_id: str


@dataclass
class DataUriInfo:
    data_uri: str


@dataclass
class DataInputInfo:
    universal_link: str
    inputs: dict

    @staticmethod
    def deserialize(data: dict):
        return DataInputInfo(universal_link=data.get("universal_link", ""), inputs=data.get("inputs", {}))


class FlowSourceType(int, Enum):
    AzureFileShare = 0
    Snapshot = 1
    DataUri = 2


@dataclass
class FlowSource:
    flow_source_type: FlowSourceType
    flow_source_info: Union[AzureFileShareInfo, SnapshotInfo]
    flow_dag_file: str

    @staticmethod
    def deserialize(data: dict) -> "FlowSource":
        flow_source = FlowSource(
            flow_source_type=FlowSourceType(data.get("flow_source_type", FlowSourceType.AzureFileShare)),
            flow_source_info=data.get("flow_source_info", {}),
            flow_dag_file=data.get("flow_dag_file", ""),
        )

        flow_source_info = flow_source.flow_source_info

        if flow_source.flow_source_type == FlowSourceType.AzureFileShare:
            flow_source.flow_source_info = AzureFileShareInfo.deserialize(flow_source_info)
        elif flow_source.flow_source_type == FlowSourceType.Snapshot:
            flow_source.flow_source_info = SnapshotInfo(snapshot_id=flow_source_info.get("snapshot_id", ""))
        else:
            raise InvalidFlowSourceType(
                message_format="Invalid flow_source_type value: {flow_source_type}",
                flow_source_type=flow_source.flow_source_type,
            )

        return flow_source


@dataclass
class MetaV2Request:
    tools: Dict[str, Dict]
    flow_source_info: Union[AzureFileShareInfo, DataUriInfo]
    flow_source_type: FlowSourceType

    @staticmethod
    def deserialize(data: dict):
        req = MetaV2Request(
            tools=data.get("tools", {}),
            flow_source_type=data.get("flow_source_type", FlowSourceType.AzureFileShare),
            flow_source_info=data.get("flow_source_info", {}),
        )
        flow_source_info = data.get("flow_source_info", {})

        if req.flow_source_type == FlowSourceType.AzureFileShare:
            req.flow_source_info = AzureFileShareInfo.deserialize(flow_source_info)
        elif req.flow_source_type == FlowSourceType.DataUri:
            req.flow_source_info = DataUriInfo(data_uri=flow_source_info.get("data_uri", ""))
        else:
            raise InvalidFlowSourceType(
                message_format="Invalid flow_source_type value for MetaV2Request: {flow_source_type}",
                flow_source_type=req.flow_source_type,
            )
        return req


@dataclass
class SubmissionRequestBaseV2:
    # Flow execution required fields
    flow_id: str
    flow_run_id: str
    flow_source: FlowSource
    connections: Dict[str, Any]

    # Runtime fields, could be optional
    log_path: Optional[str] = None
    environment_variables: Optional[Dict[str, str]] = None
    app_insights_instrumentation_key: Optional[str] = None
    predefined_policies: PredefinedPolicies = None

    @classmethod
    def deserialize(cls, data: dict):
        return cls(
            flow_id=data.get("flow_id", ""),
            flow_run_id=data.get("flow_run_id", ""),
            flow_source=FlowSource.deserialize(data.get("flow_source", {})),
            connections=data.get("connections", {}),
            log_path=data.get("log_path", ""),
            environment_variables=data.get("environment_variables", {}),
            app_insights_instrumentation_key=data.get("app_insights_instrumentation_key"),
            predefined_policies=PredefinedPolicies.deserialize(data.get("predefined_policies", {})),
        )

    def desensitize_to_json(self) -> str:
        """This function is used to desensitize request for logging."""
        ignored_keys = ["connections"]
        place_holder = "**data_scrubbed**"
        data = asdict(
            self, dict_factory=lambda x: {k: place_holder if k in ignored_keys else serialize(v) for (k, v) in x if v}
        )
        return json.dumps(data)

    def get_run_mode(self):
        raise NotImplementedError(f"Request type {self.__class__.__name__} is not implemented.")

    def get_log_filter_patterns(self):
        if self.predefined_policies is not None and self.predefined_policies.log_filtering_policy is not None:
            if self.predefined_policies.log_filtering_policy.filtering_patterns is not None:
                return self.predefined_policies.log_filtering_policy.filtering_patterns
        return []


@dataclass
class FlowRequestV2(SubmissionRequestBaseV2):
    inputs: Mapping[str, Any] = None
    output_sub_dir: str = None

    @classmethod
    def deserialize(cls, data: dict) -> "FlowRequestV2":
        req = super().deserialize(data)
        req.inputs = data.get("inputs", {})
        req.output_sub_dir = data.get("output_dir", None)
        return req

    def get_run_mode(self):
        return RunMode.Test


@dataclass
class AsyncFlowRequest(FlowRequestV2):
    azure_storage_setting: AzureStorageSetting = None
    data_inputs: Mapping[str, DataInputInfo] = None

    @classmethod
    def deserialize(cls, data: dict) -> "AsyncFlowRequest":
        req = super().deserialize(data)
        data_inputs = data.get("data_inputs", {})
        req.data_inputs = {k: DataInputInfo.deserialize(v) for k, v in data_inputs.items()}
        req.azure_storage_setting = AzureStorageSetting.deserialize(data.get("azure_storage_setting", {}))
        return req


@dataclass
class BulkRunRequestV2(SubmissionRequestBaseV2):
    batch_timeout_sec: int = None
    worker_count: int = None
    data_inputs: Mapping[str, str] = None
    inputs_mapping: Mapping[str, str] = None
    azure_storage_setting: AzureStorageSetting = None
    resume_from_run_id: str = None

    def get_run_mode(self):
        return RunMode.Batch

    @classmethod
    def deserialize(cls, data: dict) -> "BulkRunRequestV2":
        req = super().deserialize(data)
        req.batch_timeout_sec = data.get("batch_timeout_sec", None)
        req.worker_count = data.get("worker_count", None)
        req.data_inputs = data.get("data_inputs", {})
        req.inputs_mapping = data.get("inputs_mapping", {})
        req.azure_storage_setting = AzureStorageSetting.deserialize(data.get("azure_storage_setting", {}))
        req.resume_from_run_id = data.get("resume_from_run_id", None)
        return req


@dataclass
class SingleNodeRequestV2(SubmissionRequestBaseV2):
    node_name: str = None
    inputs: Mapping[str, Any] = None
    output_sub_dir: str = None

    @classmethod
    def deserialize(cls, data: dict) -> "SingleNodeRequestV2":
        req = super().deserialize(data)
        req.node_name = data.get("node_name", "")
        req.inputs = data.get("inputs", {})
        req.output_sub_dir = data.get("output_dir", None)
        return req

    def get_run_mode(self):
        return RunMode.SingleNode

    @staticmethod
    def get_node_name_from_node_inputs_key(k: str) -> str:
        """
        Node input keys might have the format: {node name}.output
        Strip .output and return node name in this case.
        """
        if k.endswith(".output"):
            return k[: -len(".output")]
        return k


@dataclass
class AsyncSingleNodeRequest(SingleNodeRequestV2):
    azure_storage_setting: AzureStorageSetting = None
    is_default_variant: bool = True
    node_variant_id: str = None
    node_output_paths: dict = None

    @classmethod
    def deserialize(cls, data: dict) -> "AsyncSingleNodeRequest":
        req = super().deserialize(data)
        req.azure_storage_setting = AzureStorageSetting.deserialize(data.get("azure_storage_setting", {}))
        req.is_default_variant = data.get("is_default_variant", True)
        req.node_variant_id = data.get("node_variant_id", None)
        req.node_output_paths = data.get("node_output_paths", {})
        return req


@dataclass
class CancelRunRequest:
    flow_run_id: str
    azure_storage_setting: AzureStorageSetting = None

    # Runtime fields, could be optional
    log_path: Optional[str] = None
    app_insights_instrumentation_key: Optional[str] = None

    @classmethod
    def deserialize(cls, data: dict) -> "CancelRunRequest":
        return cls(
            flow_run_id=data.get("flow_run_id", ""),
            log_path=data.get("log_path", ""),
            app_insights_instrumentation_key=data.get("app_insights_instrumentation_key"),
            azure_storage_setting=AzureStorageSetting.deserialize(data.get("azure_storage_setting"))
            if data.get("azure_storage_setting")
            else None,
        )
