# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------


class DefaultConfig(object):
    DEV = "dev"
    MIR = "mir"
    PYMT = "pymt"


DEFAULT_CONFIGS = [getattr(DefaultConfig, k) for k in dir(DefaultConfig) if k.isupper()]

PRT_CONFIG_FILE = "prt.yaml"

PRT_CONFIG_OVERRIDE_ENV = "PRT_CONFIG_OVERRIDE"
PRT_CONFIG_FILE_ENV = "PRT_CONFIG_FILE"
PROMPTFLOW_PROJECT_PATH = "PROMPTFLOW_PROJECT_PATH"
PROMPTFLOW_ENCODED_CONNECTIONS = "PROMPTFLOW_ENCODED_CONNECTIONS"

ENV_AZURE_ACTIVE_DIRECTORY = "AZURE_ACTIVE_DIRECTORY"
ENV_AZURE_RESOURCE_MANAGER = "AZURE_RESOURCE_MANAGER"

DEFAULT_FLOW_YAML_FILE = "flow.dag.yaml"
STORAGE_ACCOUNT_NAME = "STORAGE_ACCOUNT_NAME"
LINE_NUMBER_KEY = "line_number"
STATUS_KEY = "status"

TABLE_LIMIT_PROPERTY_SIZE = 64000  # 64 KB
TABLE_LIMIT_ENTITY_SIZE = 1000000  # 1 MB
SYNC_REQUEST_TIMEOUT_THRESHOLD = 10  # 10 seconds could be a normal timeout.
TOTAL_CHILD_RUNS_KEY = "total_child_runs"


class AzureStorageType:
    LOCAL = "local"
    TABLE = "table"
    BLOB = "blob"


class AzureMLConfig:
    SUBSCRIPTION_ID = "SUBSCRIPTION_ID"
    RESOURCE_GROUP_NAME = "RESOURCE_GROUP_NAME"
    WORKSPACE_NAME = "WORKSPACE_NAME"
    MT_ENDPOINT = "MT_ENDPOINT"

    @classmethod
    def all_values(cls):
        all_values = []
        for key, value in vars(cls).items():
            if not key.startswith("_") and isinstance(value, str):
                all_values.append(value)
        return all_values


class PromptflowEdition:
    """Promptflow runtime edition."""

    COMMUNITY = "community"
    """Community edition."""
    ENTERPRISE = "enterprise"
    """Enterprise edition."""


class ComputeType:
    MANAGED_ONLINE_DEPLOYMENT = "managed_online_deployment"
    COMPUTE_INSTANCE = "compute_instance"
    LOCAL = "local"


class RuntimeMode:
    COMPUTE = "compute"
