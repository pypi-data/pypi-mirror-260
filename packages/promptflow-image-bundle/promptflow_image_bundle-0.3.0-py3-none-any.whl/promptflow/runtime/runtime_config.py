# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from azure.core.exceptions import ClientAuthenticationError
from omegaconf import OmegaConf

from promptflow.contracts.run_mode import RunMode
from promptflow.runtime._errors import UserAuthenticationError
from promptflow.runtime.constants import ComputeType, PromptflowEdition, RuntimeMode
from promptflow.runtime.contracts.azure_storage_mode import AzureStorageMode
from promptflow.runtime.contracts.azure_storage_setting import AzureStorageSetting
from promptflow.runtime.storage.run_storage import AbstractRunStorage, DummyRunStorage
from promptflow.runtime.utils._run_history_client import RunHistoryClient
from promptflow.runtime.utils._token_utils import get_default_credential
from promptflow.runtime.utils._utils import get_mlflow_tracking_uri, is_in_ci_pipeline
from promptflow.runtime.utils.internal_logger_utils import close_telemetry_log_handler, reset_telemetry_log_handler
from promptflow.runtime.utils.retry_utils import retry
from promptflow.runtime.utils.timer import Timer

from ._errors import (
    ConfigFileNotExists,
    InvalidClientAuthentication,
    MissingDeploymentConfigs,
    UserAuthenticationValidationError,
)
from .constants import DEFAULT_CONFIGS, PRT_CONFIG_FILE_ENV, PRT_CONFIG_OVERRIDE_ENV
from .utils import get_workspace_config, logger

MISSING_DEPLOYMENT_CONFIGS_ERROR_MESSAGE = (
    "Please make sure subscription_id, resource_group, workspace_name, mt_service_endpoint are configured."
)


@dataclass
class AppConfig:
    """App config."""

    app: str
    """the starting app."""
    type: str
    """the server type, available: dev, command"""
    # dev type config
    host: str
    """host of the started server."""
    port: int
    """http port of the started server."""
    debug: bool
    """ If the debug flag is set the server will automatically \
    reload for code changes and show a debugger in case an exception happened."""
    # command type config
    args: str
    """additional command args to start server."""
    static_folder: str
    """The folder of static resources when start app."""

    def __init__(self, **kwargs):
        self.app = kwargs.get("app", "promptflow.runtime.app:app")
        self.type = kwargs.get("type", "dev")
        self.host = kwargs.get("host", "localhost")
        self.port = kwargs.get("port", 8080)
        self.debug = kwargs.get("debug", False)
        self.args = kwargs.get("args", "")
        self.static_folder = kwargs.get("static_folder", "")


@dataclass
class ExecutionConfig:
    """Execution config."""

    debug: bool
    """enable debug mode, which will print more traces."""
    execute_in_process: bool
    """ enable easier debugging by not process user request in a separate process."""

    def __init__(self, **kwargs):
        self.debug = kwargs.get("debug", True)
        self.execute_in_process = kwargs.get("execute_in_process", False)


@dataclass
class StorageConfig:
    """Execution config."""

    storage_account: str
    """storage account name to store run records, workspace default datastore will be used if not specified."""
    storage_account_key: str
    """storage account key to access storage account."""

    def __init__(self, **kwargs):
        self.storage_account = str(kwargs.get("storage_account", ""))
        self.storage_account_key = str(kwargs.get("storage_account_key", ""))


@dataclass
class DeploymentConfig:
    """Deployment config."""

    edition: str
    """deployment edition, available: community, enterprise."""
    compute_type: str
    """compute_type."""
    runtime_mode: str
    """runtime_mode, available: compute, serving."""
    subscription_id: str
    """subscription_id."""
    resource_group: str
    """resource_group."""
    workspace_name: str
    """workspace_name."""
    workspace_id: str
    """workspace_id."""
    endpoint_name: str
    """online_endpoint_name."""
    deployment_name: str
    """online_deployment_name."""
    mt_service_endpoint: str
    """mt_service_endpoint."""
    runtime_name: str
    """runtime_name."""

    def __init__(self, **kwargs):
        self.edition = kwargs.get("edition", PromptflowEdition.COMMUNITY)
        self.compute_type = kwargs.get("compute_type", ComputeType.MANAGED_ONLINE_DEPLOYMENT)
        self.runtime_mode = kwargs.get("runtime_mode", RuntimeMode.COMPUTE)
        self.subscription_id = kwargs.get("subscription_id", "")
        self.resource_group = str(kwargs.get("resource_group", ""))
        self.workspace_name = str(kwargs.get("workspace_name", ""))
        self.workspace_id = kwargs.get("workspace_id", "")
        self.endpoint_name = str(kwargs.get("endpoint_name", ""))
        self.deployment_name = str(kwargs.get("deployment_name", ""))
        self.mt_service_endpoint = kwargs.get("mt_service_endpoint", "")
        self.runtime_name = str(kwargs.get("runtime_name", ""))

    def to_logsafe_dict(self) -> Dict[str, str]:
        """Convert the config to a dict that can be logged safely."""
        return {
            "edition": self.edition,
            "compute_type": self.compute_type,
            "runtime_mode": self.runtime_mode,
            "subscription_id": self.subscription_id,
            "resource_group": self.resource_group,
            "workspace_name": self.workspace_name,
            "workspace_id": self.workspace_id,
            "runtime_name": self.runtime_name,
            "deployment_name": self.deployment_name,
            "endpoint_name": self.endpoint_name,
        }


@dataclass
class RuntimeConfig:
    """Runtime config."""

    base_dir: str
    """ working directory of the runtime. """
    app: AppConfig
    storage: StorageConfig
    execution: ExecutionConfig
    deployment: DeploymentConfig

    def __init__(self, **kwargs):
        self.base_dir = kwargs.get("base_dir", "")
        self.app = kwargs.get("app", AppConfig())
        self.storage = kwargs.get("storage", StorageConfig())
        self.execution = kwargs.get("execution", ExecutionConfig())
        self.deployment = kwargs.get("deployment", DeploymentConfig())

    def get_region(self) -> str:
        """Get workspace's region. Return empty string if exception."""
        try:
            from .utils._token_utils import get_default_credential

            # ml_client will always use default credential
            ml_client_cred = get_default_credential()
            ml_client = self.get_ml_client(ml_client_cred)

            if ml_client is None:
                return ""
            workspace = ml_client.workspaces.get(name=self.deployment.workspace_name)
            return workspace.location
        except Exception as ex:
            # Not a critical path, swallow the exception.
            logger.warning("Failed to get region. Exception: {customer_content}", extra={"customer_content": ex})
        return ""

    def _populate_default_config_from_env(self, raise_error=True):
        """get default config"""
        # use self.fully_configured to mark th
        if getattr(self, "fully_configured", False):
            return

        if not self.storage.storage_account or not self.deployment.mt_service_endpoint:
            # in compute instance we can get mlclient from env
            logger.info("Initializing runtime config from mlclient.")
            try:
                from .utils._mlclient_helper import get_mlclient_from_env

                ml_client = get_mlclient_from_env()
            except Exception:
                # if no credential found, get_mlclient_from_env will fail with ClientAuthenticationError
                # this should not block instance startup, so we'll swallow the error and raise when request comes
                ml_client = None
            if ml_client is None and self.deployment.edition == PromptflowEdition.ENTERPRISE:
                error_msg = "Failed to initialize runtime config, please authenticate if running in compute instance."
                if raise_error:
                    raise InvalidClientAuthentication(message=error_msg)
                else:
                    # swallow error since we'll try init again when receiving requests
                    logger.warning(error_msg)
                    return
            config = get_workspace_config(ml_client=ml_client, logger=logger)
            logger.info(f"Workspace config from mlclient: {config}")
            if not config:
                return
            self.storage.storage_account = self.storage.storage_account or config["storage_account"]
            self.deployment.mt_service_endpoint = self.deployment.mt_service_endpoint or config["mt_service_endpoint"]
            self.deployment.subscription_id = self.deployment.subscription_id or config["subscription_id"]
            self.deployment.resource_group = self.deployment.resource_group or config["resource_group"]
            self.deployment.workspace_name = self.deployment.workspace_name or config["workspace_name"]
            self.deployment.workspace_id = self.deployment.workspace_id or config["workspace_id"]
        self.fully_configured = True

    def post_init(self):
        """post init, resolving paths"""
        base_dir = str(self.base_dir)
        if hasattr(self.app, "port"):
            base_dir = base_dir.replace("{port}", str(self.app.port))
        wd = Path(os.getcwd()).as_posix()
        if wd.endswith(base_dir):
            # we already in the expected directory
            self.base_dir = Path(wd)
        else:
            self.base_dir = Path(base_dir).absolute()

        if not isinstance(self.app, AppConfig):
            self.app = AppConfig(**self.app)

        if not isinstance(self.storage, StorageConfig):
            self.storage = StorageConfig(**self.storage)

        if not isinstance(self.execution, ExecutionConfig):
            self.execution = ExecutionConfig(**self.execution)

        if not isinstance(self.deployment, DeploymentConfig):
            self.deployment = DeploymentConfig(**self.deployment)

        if self.deployment.edition == PromptflowEdition.ENTERPRISE:
            self._populate_default_config_from_env(raise_error=False)
            self._add_workspace_info_to_environ()
            self._add_cloud_name_to_environ()

    def init_from_request(self, workspace_access_token=None):
        """init from request"""
        if not self.storage.storage_account_key or not self.deployment.workspace_id:
            try:
                with Timer(logger, "Initializing mlclient from request"):
                    from .utils._token_utils import get_default_credential, get_echo_credential_from_token

                    if workspace_access_token:
                        # get the storage key from workspace, so no need to configure storage table access to compute
                        logger.info("Init from request using workspace access token")
                        cred = get_echo_credential_from_token(workspace_access_token, print_diagnostic=True)
                    else:
                        logger.info("Init from request using default credential")
                        cred = get_default_credential()

                    ml_client = self.get_ml_client(cred)
            except Exception as e:
                # ignore error, best effort
                logger.warning("Failed to get mlclient: {customer_content}", extra={"customer_content": e})
                ml_client = None

            if ml_client and not self.storage.storage_account_key:
                try:
                    with Timer(logger, "Getting storage account key"):
                        keys = ml_client.workspaces._operation.list_keys(
                            ml_client.workspaces._resource_group_name, ml_client.workspaces._default_workspace_name
                        )
                        self.storage.storage_account_key = keys.user_storage_key
                except Exception as e:
                    # ignore expected error in managed online deployment runtime
                    if self.deployment.compute_type != ComputeType.MANAGED_ONLINE_DEPLOYMENT:
                        logger.warning(
                            "Failed to get storage account key: {customer_content}", extra={"customer_content": e}
                        )

            if ml_client and not self.deployment.workspace_id:
                try:
                    with Timer(logger, "Getting workspace id"):
                        config = get_workspace_config(ml_client=ml_client, logger=logger)
                        logger.info(f"Workspace config from mlclient: {config}")
                        self.deployment.workspace_id = config["workspace_id"]
                except Exception as e:
                    logger.warning("Failed to get workspace id: {customer_content}", extra={"customer_content": str(e)})

        if self.deployment.edition == PromptflowEdition.ENTERPRISE:
            # init again to avoid case when user authenticate the ci after PRT starts.
            self._populate_default_config_from_env()
            self._add_workspace_info_to_environ()
            self._add_cloud_name_to_environ()

    def _add_workspace_info_to_environ(self):
        # inject workspace information into environment variables
        # this is required for identity based connection
        os.environ["AZUREML_ARM_SUBSCRIPTION"] = self.deployment.subscription_id
        os.environ["AZUREML_ARM_RESOURCEGROUP"] = self.deployment.resource_group
        os.environ["AZUREML_ARM_WORKSPACE_NAME"] = self.deployment.workspace_name

    def _add_cloud_name_to_environ(self):
        """Update cloud env for all types of azure cloud."""
        from azure.ai.ml._azure_environments import _get_default_cloud_name, _set_cloud

        cloud_name = os.environ.get("AML_CloudName")  # CI set "AML_CloudName" env
        if cloud_name is None:
            # if not found, get cloud name from "AZUREML_CURRENT_CLOUD" env or default public "AzureCloud"
            cloud_name = _get_default_cloud_name()
        try:
            # update cloud name so that SDK (like MLClient) can use correct endpoint
            _set_cloud(cloud_name)
            logger.info(f"Set cloud name to {cloud_name}")
        except Exception as e:
            logger.warning(f"Failed to set cloud name to {cloud_name}: {e}")

    # TODO: Remove this method because get_azure_ml_run_storage_v2 already exists.
    def get_run_storage(
        self,
        workspace_access_token=None,
        azure_storage_setting: AzureStorageSetting = None,
        run_mode: RunMode = None,
        output_dir: Path = None,
    ) -> AbstractRunStorage:
        """get run storage."""
        if azure_storage_setting and azure_storage_setting.azure_storage_mode == AzureStorageMode.Blob:
            if self.deployment.edition == PromptflowEdition.ENTERPRISE and run_mode != RunMode.Batch:
                logger.info("Using dummy run storage for non-bulk test run in Enterprise edition")
                return DummyRunStorage()

            from .utils._token_utils import get_default_credential

            logger.info("Setting mlflow tracking uri...")
            mlflow_tracking_uri = self.set_mlflow_tracking_uri()

            # ml_client will always use default credential
            ml_client_cred = get_default_credential()
            ml_client = self.get_ml_client(ml_client_cred)

            logger.info("Validating 'AzureML Data Scientist' user authentication...")
            self.validate_user_authentication_by_ml_client(ml_client)

            asset_client = self.get_asset_client()
            artifact_client = self.get_artifact_client()

            logger.info("Using AzureMLRunStorageV2")
            return self.get_azure_ml_run_storage_v2(
                azure_storage_setting=azure_storage_setting,
                mlflow_tracking_uri=mlflow_tracking_uri,
                asset_client=asset_client,
                artifact_client=artifact_client,
                output_dir=output_dir,
            )
        else:
            logger.info("Using dummy run storage when azure_storage_mode is not blob.")
            return DummyRunStorage()

    def get_azure_ml_run_storage_v2(
        self,
        azure_storage_setting: AzureStorageSetting,
        mlflow_tracking_uri: str,
        asset_client,
        artifact_client,
        output_dir: Path = None,
    ):
        from promptflow.runtime.storage.azureml_run_storage_v2 import AzureMLRunStorageV2

        return AzureMLRunStorageV2(
            azure_storage_setting=azure_storage_setting,
            mlflow_tracking_uri=mlflow_tracking_uri,
            asset_client=asset_client,
            artifact_client=artifact_client,
            output_dir=output_dir,
        )

    def validate_user_authentication_by_ml_client(self, ml_client):
        """Test if current runtime has access to perform workspace run operations"""
        from azure.core.exceptions import HttpResponseError, ResourceNotFoundError

        from promptflow.runtime.storage.run_storage import RuntimeAuthErrorType

        try:
            # get a dummy run to test the auth
            self.validate_by_get_dummy_run(ml_client)
        except Exception as e:
            msg = str(e)
            if isinstance(e, ResourceNotFoundError) and e.status_code == 404:
                # if return not found error, it's by-design and proves the auth is fine
                logger.info("Successfully validated 'AzureML Data Scientist' user authentication.")
                return
            elif isinstance(e, HttpResponseError) and e.status_code == 403:
                auth_error_message = self._get_auth_error_message(RuntimeAuthErrorType.WORKSPACE)
                logger.error(
                    auth_error_message + " Original error: {customer_content}", extra={"customer_content": msg}
                )
                # if it's auth issue, return auth_error_message
                raise UserAuthenticationError(message=auth_error_message) from e

            raise UserAuthenticationValidationError(
                message_format=f"Failed to perform workspace run operations: {msg}", msg=msg
            ) from e

    @retry(ClientAuthenticationError, tries=5, delay=0.5, backoff=1, logger=logger)
    def validate_by_get_dummy_run(self, ml_client):
        ml_client.jobs._runs_operations.get_run(run_id="dummy")

    def set_mlflow_tracking_uri(self):
        """Get and set the mlflow tracking uri"""

        # After importing mlflow, telemetry log handler needs to be reset,
        # otherwise logs will be missing. This is caused by a conflict between mlflow and app insights.
        close_telemetry_log_handler(logger)
        import mlflow

        reset_telemetry_log_handler(logger)

        deployment = self.deployment
        if (
            not deployment.subscription_id
            or not deployment.resource_group
            or not deployment.workspace_name
            or not deployment.mt_service_endpoint
        ):
            raise MissingDeploymentConfigs(
                message_format="Missing necessary deployment configs, below configs cannot be none or empty: "
                "Subscription ID: {subscription_id}. "
                "Resource group name: {resource_group}. "
                "Workspace name: {workspace_name}. "
                "Mt_service_endpoint: {mt_service_endpoint}.",
                subscription_id=deployment.subscription_id,
                resource_group=deployment.resource_group,
                workspace_name=deployment.workspace_name,
                mt_service_endpoint=deployment.mt_service_endpoint,
            )
        mlflow_tracking_uri = get_mlflow_tracking_uri(
            subscription_id=deployment.subscription_id,
            resource_group_name=deployment.resource_group,
            workspace_name=deployment.workspace_name,
            mt_endpoint=deployment.mt_service_endpoint,
        )

        # this is to enable mlflow to use CI SP client credential
        # Refer to: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-mlflow-configure-tracking?view=azureml-api-2&tabs=python%2Cmlflow#configure-authentication  # noqa: E501
        if is_in_ci_pipeline():
            os.environ["AZURE_TENANT_ID"] = os.environ.get("tenantId")
            os.environ["AZURE_CLIENT_ID"] = os.environ.get("servicePrincipalId")
            os.environ["AZURE_CLIENT_SECRET"] = os.environ.get("servicePrincipalKey")

        # set tracking uri
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        return mlflow_tracking_uri

    def get_ml_client(self, credential, subscription_id=None, resource_group=None, workspace_name=None):
        """get ml client."""
        if subscription_id is None:
            subscription_id = self.deployment.subscription_id
        if resource_group is None:
            resource_group = self.deployment.resource_group
        if workspace_name is None:
            workspace_name = self.deployment.workspace_name
        if subscription_id and resource_group and workspace_name:
            from azure.ai.ml import MLClient

            return MLClient(
                subscription_id=subscription_id,
                resource_group_name=resource_group,
                workspace_name=workspace_name,
                credential=credential,
            )

        raise MissingDeploymentConfigs(
            message_format="Please make sure subscription_id, resource_group, workspace_name are configured."
        )

    def get_snapshot_client(self):
        from promptflow.runtime.utils._snapshots_client import SnapshotsClient

        subscription_id = self.deployment.subscription_id
        resource_group = self.deployment.resource_group
        workspace_name = self.deployment.workspace_name
        mt_service_endpoint = self.deployment.mt_service_endpoint
        if subscription_id and resource_group and workspace_name and mt_service_endpoint:
            return SnapshotsClient(runtime_config=self)
        raise MissingDeploymentConfigs(message_format=MISSING_DEPLOYMENT_CONFIGS_ERROR_MESSAGE)

    def get_run_history_client(self) -> RunHistoryClient:
        subscription_id = self.deployment.subscription_id
        resource_group = self.deployment.resource_group
        workspace_name = self.deployment.workspace_name
        mt_service_endpoint = self.deployment.mt_service_endpoint
        if subscription_id and resource_group and workspace_name and mt_service_endpoint:

            return RunHistoryClient(
                subscription_id=self.deployment.subscription_id,
                resource_group=self.deployment.resource_group,
                workspace_name=self.deployment.workspace_name,
                service_endpoint=self.deployment.mt_service_endpoint,
                credential=get_default_credential(),
                runtime_config=self,
            )
        raise MissingDeploymentConfigs(message_format=MISSING_DEPLOYMENT_CONFIGS_ERROR_MESSAGE)

    def get_artifact_client(self):
        from promptflow.runtime.utils._artifact_client import ArtifactClient

        subscription_id = self.deployment.subscription_id
        resource_group = self.deployment.resource_group
        workspace_name = self.deployment.workspace_name
        mt_service_endpoint = self.deployment.mt_service_endpoint
        if subscription_id and resource_group and workspace_name and mt_service_endpoint:
            return ArtifactClient.init_from_runtime_config(self)
        raise MissingDeploymentConfigs(message_format=MISSING_DEPLOYMENT_CONFIGS_ERROR_MESSAGE)

    def get_asset_client(self):
        from promptflow.runtime.utils._asset_client import AssetClient

        subscription_id = self.deployment.subscription_id
        resource_group = self.deployment.resource_group
        workspace_name = self.deployment.workspace_name
        mt_service_endpoint = self.deployment.mt_service_endpoint
        if subscription_id and resource_group and workspace_name and mt_service_endpoint:
            return AssetClient.init_from_runtime_config(self)
        raise MissingDeploymentConfigs(message_format=MISSING_DEPLOYMENT_CONFIGS_ERROR_MESSAGE)

    def get_compute_info(self):
        """Get compute name. note ci name and endpoint name share the same config value deployment.endpoint_name."""
        # both endpoint and ci should use this config value, fallback to get value from env var in case it's not set
        compute_name = self.deployment.endpoint_name or os.environ.get("CI_NAME", None)
        if not compute_name:
            logger.warning(f"Deployment's endpoint name is not properly configured. Got {compute_name!r}")

        return compute_name

    def _get_auth_error_message(self, error_type) -> str:
        """Get auth error message for workspace/storage auth error, and for endpoint/ci compute."""
        from promptflow.runtime.storage.run_storage import RuntimeAuthErrorType

        compute_name = self.get_compute_info()
        compute_type = self.deployment.compute_type
        storage_account = self.storage.storage_account
        auth_error_suffix = "More details can be found in https://aka.ms/pf-runtime."
        auth_error_messages = {
            ComputeType.MANAGED_ONLINE_DEPLOYMENT: {
                RuntimeAuthErrorType.WORKSPACE: (
                    "Failed to perform workspace run operations due to invalid authentication. "
                    f"Please assign RBAC role 'AzureML Data Scientist' to the managed online endpoint "
                    f"{compute_name!r}, and wait for a few minutes to make sure the new role takes effect. "
                    f"{auth_error_suffix}"
                ),
                RuntimeAuthErrorType.STORAGE: (
                    "Failed to perform table/blob operations due to invalid authentication. "
                    "Please assign RBAC role 'Storage Table Data Contributor' and 'Storage Blob Data Contributor' "
                    f"of the storage account {storage_account!r} to the managed online endpoint {compute_name!r}, "
                    f"and wait for a few minutes to make sure the new role takes effect. {auth_error_suffix}"
                ),
            },
            ComputeType.COMPUTE_INSTANCE: {
                RuntimeAuthErrorType.WORKSPACE: (
                    "Failed to perform workspace run operations due to invalid authentication. "
                    f"Please assign RBAC role 'AzureML Data Scientist' to your user account, "
                    f"wait for a few minutes to let the new role takes effect, and make sure your "
                    f"compute is authenticated. To authenticate the compute, "
                    f"open arbitrary ipynb file in CI notebook and click the authentication button. {auth_error_suffix}"
                ),
                RuntimeAuthErrorType.STORAGE: (
                    "Failed to perform table/blob operations due to invalid authentication. "
                    "Please assign RBAC role 'Storage Table Data Contributor' and 'Storage Blob Data Contributor' "
                    f"of the storage account {storage_account!r} to your user account, "
                    f"wait for a few minutes to let the new role takes effect, and make sure your "
                    f"compute is authenticated. To authenticate the compute, "
                    f"open arbitrary ipynb file in CI notebook and click the authentication button. {auth_error_suffix}"
                ),
            },
        }

        if compute_type not in (ComputeType.MANAGED_ONLINE_DEPLOYMENT, ComputeType.COMPUTE_INSTANCE):
            error_info = (
                f"Invalid compute type {compute_type!r}, should be "
                f"{ComputeType.MANAGED_ONLINE_DEPLOYMENT!r} or {ComputeType.COMPUTE_INSTANCE!r}."
            )
            logger.error(error_info)
            return error_info

        return auth_error_messages[compute_type][error_type]

    def to_yaml(self) -> str:
        """convert config to yaml."""
        return OmegaConf.to_yaml(self)

    def __hash__(self) -> int:
        """Implement this so it can be used as an parameter in @lru_cache."""
        return hash(self.to_yaml())


def load_runtime_config(file=None, args=None) -> RuntimeConfig:
    """load runtime config from file."""
    # TODO add support for overrides
    if file is None:
        # Use enterprise-on-local.yaml for enterprise version local testing.
        file = Path(__file__).parent / "config/dev.yaml"

    if file in DEFAULT_CONFIGS:
        file = Path(__file__).parent / f"config/{file}.yaml"

    if isinstance(file, str):
        file = Path(file)

    logger.info("Load config file: %s", file)
    if not file.exists():
        raise ConfigFileNotExists(message_format="Please make sure config file exists: {file}", file=str(file))
    conf = OmegaConf.load(file)

    if args is None:
        args = []
    additional_conf = OmegaConf.from_cli(args)
    env_conf = os.environ.get(PRT_CONFIG_OVERRIDE_ENV)
    if env_conf:
        logger.info("Merge additional_conf: {customer_content}", extra={"customer_content": env_conf})
        env_conf = env_conf.split(",")
        env_conf = OmegaConf.from_dotlist(env_conf)
        additional_conf.merge_with(env_conf)

    model_dir = os.environ.get("AZUREML_MODEL_DIR", None)
    env_file = os.environ.get(PRT_CONFIG_FILE_ENV, None)
    if model_dir and env_file:
        env_file = Path(model_dir) / env_file
        logger.info("Merge additional_conf: %s", env_file)
        env_conf = OmegaConf.load(env_file)
        additional_conf.merge_with(env_conf)
    conf.merge_with(additional_conf)
    logger.debug("Loaded config:\n {customer_content}", extra={"customer_content": OmegaConf.to_yaml(conf)})
    # compute_type default is 'managed_online_deployment'; 'local' compute_type will be given from yaml;
    # if CI_NAME is set, compute_type is 'compute_instance'.
    if not conf.get("deployment.compute_type", None) and os.environ.get("CI_NAME"):
        compute_type = ComputeType.COMPUTE_INSTANCE
        conf.merge_with(OmegaConf.from_dotlist([f"deployment.compute_type={compute_type}"]))
        logger.debug("Set config: deployment.compute_type=%s", compute_type)

    # Check if running enterprise edition locally，if so, generate the uri from config.json and set MLFLOW_TRACKING_URI
    if (
        conf.get("deployment", {}).get("compute_type") == ComputeType.LOCAL
        and conf.get("deployment", {}).get("edition") == PromptflowEdition.ENTERPRISE
        and conf.get("deployment", {}).get("tag") == "enterprise-dev"
    ):
        print("Enterprise edition locally.")
        config_file = Path(__file__).parent / "config/config.json"
        if config_file.exists():
            # The URI generated at this time is not a real MLflow tracking URI. We only extract the subscription_ID,
            # resource_group and workspace_name from the URI to create a mlclient.
            os.environ["MLFLOW_TRACKING_URI"] = get_azureml_workspace_uri(config_file)
        else:
            raise ConfigFileNotExists(
                message_format="Please make sure config.json file exists: {file}", file=str(config_file)
            )

    config = RuntimeConfig(**conf)
    if config.base_dir == "":
        config.base_dir = Path(file).parent.absolute()

    config.post_init()
    logger.info("Full config:\n {customer_content}", extra={"customer_content": config.to_yaml()})

    return config


def get_azureml_workspace_uri(config_file):
    """get azureml workspace uri."""
    import json

    with open(config_file, "r") as f:
        config = json.load(f)
        subscription_id = config["subscription_id"]
        resource_group = config["resource_group"]
        workspace_name = config["workspace_name"]
        workspace_uri = (
            f"azureml://subscriptions/{subscription_id}/resourceGroups/{resource_group}/"
            f"providers/Microsoft.MachineLearningServices/workspaces/{workspace_name}"
        )
        return workspace_uri
