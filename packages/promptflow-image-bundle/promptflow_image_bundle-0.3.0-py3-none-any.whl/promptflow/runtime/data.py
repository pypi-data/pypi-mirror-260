""" download or mount remote data in runtime """
import os
import re
import shutil
from pathlib import Path

import requests
from azure.ai.ml.exceptions import ErrorCategory, MlException
from azure.core.exceptions import HttpResponseError, ServiceResponseError

from promptflow.exceptions import PromptflowException
from promptflow.runtime.utils import logger
from promptflow.runtime.utils.downloader import (
    DownloadDataSystemError,
    DownloadDataUserError,
    download_fileshare_data,
    get_target_file_path,
)
from promptflow.runtime.utils.retry_utils import retry

from ._errors import (
    InvalidAmlDataUri,
    InvalidBlobDataUri,
    InvalidDataUri,
    InvalidRegistryDataUri,
    InvalidWasbsDataUri,
    RuntimeConfigNotProvided,
)
from .runtime_config import RuntimeConfig

SHORT_DATASTORE_URI_REGEX_FORMAT = "azureml://datastores/([^/]+)/paths/(.+)"
LONG_DATASTORE_URI_REGEX_FORMAT = (
    "azureml://subscriptions/([^/]+)/resource[gG]roups/([^/]+)/workspaces/([^/]+)/datastores/([^/]+)/paths/(.+)"
)
JOB_URI_REGEX_FORMAT = "azureml://jobs/([^/]+)/outputs/([^/]+)/paths/(.+)"

DATA_ASSET_ID_REGEX_FORMAT = (
    "azureml://subscriptions/([^/]+)/resource[gG]roups/([^/]+)/workspaces/([^/]+)/data/([^/]+)/versions/(.+)"
)
DATA_ASSET_ID_LABEL_REGEX_FORMAT = (
    "azureml://subscriptions/([^/]+)/resource[gG]roups/([^/]+)/workspaces/([^/]+)/data/([^/]+)/labels/(.+)"
)
ASSET_ARM_ID_REGEX_FORMAT = (
    "azureml:/subscriptions/([^/]+)/resource[gG]roups/([^/]+)/"
    "providers/Microsoft.MachineLearningServices/workspaces/([^/]+)/([^/]+)/([^/]+)/versions/(.+)"
)
AZUREML_VERSION_REGEX_FORMAT = "azureml:([^/]+):(.+)"
AZUREML_LABEL_REGEX_FORMAT = "azureml:([^/]+)@(.+)"

REGISTRY_ASSET_LABEL_REGEX_FORMAT = "azureml://registries/([^/]+)/data/([^/]+)/labels/([^/]+)"
REGISTRY_ASSET_VERSION_REGEX_FORMAT = "azureml://registries/([^/]+)/data/([^/]+)/versions/([^/]+)"


WASBS_REGEX_FORMAT = "wasbs://([^@]+)@([^/]+)/(.+)"


def _wasbs_to_http_url(wasbs_url: str) -> str:
    """convert wasbs url to http url"""
    if not wasbs_url.startswith("wasbs"):
        return wasbs_url

    m = re.match(WASBS_REGEX_FORMAT, wasbs_url)
    if m is None:
        raise InvalidWasbsDataUri(message_format="Invalid wasbs data url: {wasbs_url}", wasbs_url=wasbs_url)

    container, account, path = m.groups()
    return f"https://{account}/{container}/{path}"


BLOB_HTTP_REGEX_FORMAT = "https://([^/]+)/([^/]+)/(.+)"


def _http_to_wasbs_url(url: str) -> str:
    """convert http url to wasbs url"""

    m = re.match(BLOB_HTTP_REGEX_FORMAT, url)
    if m is None:
        raise InvalidBlobDataUri(message_format="Invalid blob data url: {blob_url}", blob_url=url)

    account, container, path = m.groups()
    return f"wasbs://{container}@{account}/{path}"


def _download_blob(uri, destination, credential) -> str:
    uri = _wasbs_to_http_url(uri)
    target_file = get_target_file_path(uri=uri, destination=destination)

    from azure.storage.blob import BlobClient

    blob_client = BlobClient.from_blob_url(blob_url=uri, credential=credential)
    with open(target_file, "wb") as my_blob:
        blob_data = blob_client.download_blob()
        blob_data.readinto(my_blob)

    return target_file


def _download_blob_directory(uri, destination, credential) -> str:
    from urllib.parse import urlparse, urlunparse

    from azure.ai.ml._restclient.v2022_10_01.models import DatastoreType
    from azure.ai.ml._utils._storage_utils import get_artifact_path_from_storage_url, get_storage_client

    m = re.match(BLOB_HTTP_REGEX_FORMAT, uri)
    if m is None:
        raise InvalidBlobDataUri(message_format="Invalid blob data url: {blob_url}", blob_url=uri)

    account, container, path = m.groups()
    parsed_url = urlparse(uri)

    account_url = "https://" + account
    if parsed_url.query:
        # Use sas token instead of credential when there is sas token query
        account_url += "?" + parsed_url.query
        new_url = parsed_url._replace(query="")
        uri = urlunparse(new_url)
        credential = None

    starts_with = get_artifact_path_from_storage_url(blob_url=str(uri), container_name=container)
    storage_client = get_storage_client(
        credential=credential,
        container_name=container,
        storage_account=account,
        account_url=account_url,
        storage_type=DatastoreType.AZURE_BLOB,
    )
    storage_client.download(starts_with=starts_with, destination=destination)
    return destination


def _download_public_http_url(url, destination) -> str:
    target_file = get_target_file_path(uri=url, destination=destination)

    with requests.get(url, stream=True) as r:
        with open(target_file, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return target_file


def _download_aml_uri(uri, destination, credential, runtime_config: RuntimeConfig) -> str:  # noqa: C901
    if not runtime_config and not (uri.startswith("azureml://") or uri.startswith("azureml:/subscriptions/")):
        raise RuntimeConfigNotProvided(message_format="Runtime_config must be provided for short form uri")
    # hide imports not for community version
    from azure.ai.ml import MLClient
    from azure.ai.ml._artifacts._artifact_utilities import download_artifact_from_aml_uri
    from azure.ai.ml._restclient.v2022_10_01.models import DatastoreType
    from azure.ai.ml.entities import Data

    # asset URI: resolve as datastore uri
    data: Data = None
    if re.match(ASSET_ARM_ID_REGEX_FORMAT, uri):
        sub, rg, ws, _, name, version = re.match(ASSET_ARM_ID_REGEX_FORMAT, uri).groups()
        ml_client = MLClient(credential=credential, subscription_id=sub, resource_group_name=rg, workspace_name=ws)
        data = ml_client.data.get(name, version=version)
    elif re.match(AZUREML_VERSION_REGEX_FORMAT, uri):
        name, version = re.match(AZUREML_VERSION_REGEX_FORMAT, uri).groups()
        ml_client = runtime_config.get_ml_client(credential)
        data = ml_client.data.get(name, version=version)
    elif re.match(AZUREML_LABEL_REGEX_FORMAT, uri):
        name, label = re.match(AZUREML_LABEL_REGEX_FORMAT, uri).groups()
        ml_client = runtime_config.get_ml_client(credential)
        data = ml_client.data.get(name, label=label)
    elif re.match(DATA_ASSET_ID_REGEX_FORMAT, uri):
        # asset URI: long versions
        sub, rg, ws, name, version = re.match(DATA_ASSET_ID_REGEX_FORMAT, uri).groups()
        ml_client = MLClient(credential=credential, subscription_id=sub, resource_group_name=rg, workspace_name=ws)
        data = ml_client.data.get(name, version=version)
    elif re.match(DATA_ASSET_ID_LABEL_REGEX_FORMAT, uri):
        sub, rg, ws, name, label = re.match(DATA_ASSET_ID_LABEL_REGEX_FORMAT, uri).groups()
        ml_client = MLClient(credential=credential, subscription_id=sub, resource_group_name=rg, workspace_name=ws)
        data = ml_client.data.get(name, label=label)

    if data:
        uri = str(data.path)

    # remove trailing slash all the time: it will break download file, and no slash won't break folder
    uri = uri.rstrip("/")
    # we have observed glob like uri including "**/" that will break download;
    # as we remove slash above, only check & remove "**" here.
    if uri.endswith("**"):
        uri = uri[:-2]

    # datastore uri
    if re.match(SHORT_DATASTORE_URI_REGEX_FORMAT, uri):
        datastore_name, _ = re.match(SHORT_DATASTORE_URI_REGEX_FORMAT, uri).groups()
        ml_client = runtime_config.get_ml_client(credential)
    elif re.match(LONG_DATASTORE_URI_REGEX_FORMAT, uri):
        sub, rg, ws, datastore_name, _ = re.match(LONG_DATASTORE_URI_REGEX_FORMAT, uri).groups()
        ml_client = MLClient(credential=credential, subscription_id=sub, resource_group_name=rg, workspace_name=ws)
    else:
        raise InvalidAmlDataUri(message_format="Invalid aml data uri: {aml_uri}", aml_uri=uri)

    # set include_secrets to True to get the datastore with token
    datastore = ml_client.datastores.get(datastore_name, include_secrets=True)

    if datastore.type == DatastoreType.AZURE_FILE:
        return download_fileshare_data(uri, destination, datastore)

    # download all files in the datastore starts with the url
    return download_artifact_from_aml_uri(uri, destination, ml_client.datastores)


def _download_registry_asset(uri: str, destination: str, credential) -> str:
    from azure.ai.ml import MLClient

    if re.match(REGISTRY_ASSET_LABEL_REGEX_FORMAT, uri):
        registry, name, label = re.match(REGISTRY_ASSET_LABEL_REGEX_FORMAT, uri).groups()
        ml_client = MLClient(credential=credential, registry_name=registry)
        data = ml_client.data.get(name, label=label)
    elif re.match(REGISTRY_ASSET_VERSION_REGEX_FORMAT, uri):
        registry, name, version = re.match(REGISTRY_ASSET_VERSION_REGEX_FORMAT, uri).groups()
        ml_client = MLClient(credential=credential, registry_name=registry)
        data = ml_client.data.get(name, version=version)
    else:
        raise InvalidRegistryDataUri(message_format="Invalid registry data asset uri: {uri}", uri=uri)

    if data is None or data.path is None:
        raise InvalidRegistryDataUri(message_format="Invalid registry data asset: {uri} get null data", uri=uri)

    # Need new version sdk to download registry data
    if not hasattr(ml_client, "_service_client_10_2023"):
        raise DownloadDataUserError("Not support download registry data when azure-ai-ml < 12.0")

    # Registry data is not supported to download directly with default permission.
    # - storage account of registry is in managed resource group.
    # - the permission of registry is not inherited by managed resource group.
    # Need to use sas_uri to download. We get sas_uri first
    from azure.ai.ml._restclient.v2023_10_01.models import (
        GetBlobReferenceSASRequestDto,
        GetBlobReferenceSASResponseDto,
        SASCredential,
    )

    blob_ref: GetBlobReferenceSASResponseDto = (
        ml_client._service_client_10_2023.registry_data_references.get_blob_reference_sas(
            resource_group_name=ml_client.resource_group_name,
            registry_name=registry,
            name=data.name,
            version=data.version,
            body=GetBlobReferenceSASRequestDto(asset_id=data.id, blob_uri=str(data.path)),
        )
    )
    if (
        blob_ref is None
        or blob_ref.blob_reference_for_consumption is None
        or blob_ref.blob_reference_for_consumption.credential is None
        or not isinstance(blob_ref.blob_reference_for_consumption.credential, SASCredential)
    ):
        raise DownloadDataSystemError("Failed to get sas_uri for registry data")
    sas_uri = blob_ref.blob_reference_for_consumption.credential.sas_uri
    if sas_uri is None:
        raise DownloadDataSystemError("Get empty sas_uri registry data")

    from urllib.parse import urlparse

    from azure.ai.ml._restclient.v2022_10_01.models import DatastoreType
    from azure.ai.ml._utils._storage_utils import get_artifact_path_from_storage_url, get_storage_client

    m = re.match(BLOB_HTTP_REGEX_FORMAT, data.path)
    if m is None:
        raise InvalidBlobDataUri(message_format="Invalid blob data url: {blob_url}", blob_url=data.path)

    account, container, _ = m.groups()
    parsed_url = urlparse(sas_uri)

    # Sas_url has no path, we only use the query token
    account_url = "https://" + account + "?" + parsed_url.query
    starts_with = get_artifact_path_from_storage_url(blob_url=str(data.path), container_name=container)
    storage_client = get_storage_client(
        credential=None,
        container_name=container,
        storage_account=account,
        account_url=account_url,
        storage_type=DatastoreType.AZURE_BLOB,
    )
    storage_client.download(starts_with=starts_with, destination=destination)
    return destination


@retry(DownloadDataSystemError, tries=3, logger=logger)
def prepare_data(uri: str, destination: str = None, credential=None, runtime_config: RuntimeConfig = None) -> str:
    """prepare data from blob_uri to local_file.

    Only support download now. TODO: support mount.
    Args:
        uri: uri of the data
        destination: local folder to download or mount data
        credential: credential to access remote storage

    Returns: prepared local path
    """
    # convert to str in case not
    try:
        uri = str(uri)
        destination = str(destination)

        Path(destination).mkdir(
            parents=True, exist_ok=True
        )  # CodeQL [SM01305] Safe use per destination is set by PRT service not by end user

        from .utils._token_utils import get_default_credential

        if uri.startswith("azureml://registries/"):
            if credential is None:
                credential = get_default_credential()
            # registry has no concept of datastore, cannot use the common logic of aml uri
            return _download_registry_asset(uri, destination, credential)
        if uri.startswith("azureml:"):
            if credential is None:
                credential = get_default_credential()
            # asset & datastore uri
            return _download_aml_uri(uri, destination, credential, runtime_config)
        if uri.startswith("wasbs:"):
            # storage blob uri
            if credential is None:
                credential = get_default_credential()
            return _download_blob(uri, destination, credential)
        if uri.startswith("http"):
            # public http url
            return _download_public_http_url(uri, destination)
        if os.path.exists(uri):
            # local file
            return uri
        else:
            raise InvalidDataUri(message_format="Invalid data uri: {uri}", uri=uri)
    except HttpResponseError as ex:
        logger.error(
            "Prepare data failed. StatusCode=%s. Exception={customer_content}",
            ex.status_code,
            extra={"customer_content": ex},
            exc_info=True,
        )
        if ex.status_code is not None and ex.status_code // 100 == 4:
            raise DownloadDataUserError(f"Prepare data failed. {str(ex)}") from ex
        else:
            raise DownloadDataSystemError(f"Prepare data failed. {str(ex)}") from ex
    except MlException as ex:
        logger.error(
            "Prepare data failed. Target=%s. Message=%s. Category=%s. Exception={customer_content}",
            ex.target,
            ex.no_personal_data_message,
            ex.error_category,
            extra={"customer_content": ex},
            exc_info=True,
        )
        if ex.error_category is not None and ex.error_category == ErrorCategory.USER_ERROR:
            raise DownloadDataUserError(f"Prepare data failed. {str(ex)}") from ex
        else:
            raise DownloadDataSystemError(f"Prepare data failed. {str(ex)}") from ex
    except ServiceResponseError as ex:
        logger.error(
            "Prepare data failed. Exception={customer_content}",
            extra={"customer_content": ex},
            exc_info=True,
        )
        raise DownloadDataSystemError(f"Prepare data failed. {str(ex)}") from ex
    except Exception as ex:
        if isinstance(ex, PromptflowException):
            raise ex
        logger.error(
            "Prepare data failed with exception={customer_content}",
            extra={"customer_content": ex},
            exc_info=True,
        )
        raise DownloadDataSystemError(f"Prepare data failed. {str(ex)}") from ex


@retry(DownloadDataSystemError, tries=3, logger=logger)
def prepare_blob_directory(
    uri: str, destination: str = None, credential=None, runtime_config: RuntimeConfig = None
) -> str:
    try:
        from .utils._token_utils import get_default_credential

        os.makedirs(destination, exist_ok=True)
        if uri.startswith("wasbs:"):
            uri = _wasbs_to_http_url(uri)
        if uri.startswith("http"):
            if credential is None:
                credential = get_default_credential()
            return _download_blob_directory(uri, destination, credential)
        else:
            return prepare_data(uri, destination, credential, runtime_config)
    except HttpResponseError as ex:
        logger.error(
            "Prepare blob directory failed. StatusCode=%s. Exception={customer_content}",
            ex.status_code,
            extra={"customer_content": ex},
            exc_info=True,
        )
        if ex.status_code is not None and ex.status_code // 100 == 4:
            raise DownloadDataUserError(f"Prepare blob directory failed. {str(ex)}") from ex
        else:
            raise DownloadDataSystemError(f"Prepare blob directory failed. {str(ex)}") from ex
    except MlException as ex:
        logger.error(
            "Prepare blob directory failed. Target=%s. Message=%s. Category=%s. Exception={customer_content}",
            ex.target,
            ex.no_personal_data_message,
            ex.error_category,
            extra={"customer_content": ex},
            exc_info=True,
        )
        if ex.error_category is not None and ex.error_category == ErrorCategory.USER_ERROR:
            raise DownloadDataUserError(f"Prepare blob directory failed. {str(ex)}") from ex
        else:
            raise DownloadDataSystemError(f"Prepare blob directory failed. {str(ex)}") from ex
    except ServiceResponseError as ex:
        logger.error(
            "Prepare blob directory failed. Exception={customer_content}",
            extra={"customer_content": ex},
            exc_info=True,
        )
        raise DownloadDataSystemError(f"Prepare blob directory failed. {str(ex)}") from ex
