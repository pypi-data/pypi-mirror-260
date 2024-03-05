import os

from azure.ai.ml._artifacts._fileshare_storage_helper import recursive_download
from azure.ai.ml._azure_environments import _get_storage_endpoint_from_metadata
from azure.ai.ml._utils._storage_utils import AzureMLDatastorePathUri
from azure.ai.ml.constants._common import STORAGE_ACCOUNT_URLS
from azure.ai.ml.entities._credentials import AccountKeyConfiguration
from azure.ai.ml.entities._datastore.datastore import Datastore
from azure.storage.fileshare import ShareDirectoryClient, ShareFileClient

from promptflow.exceptions import ErrorTarget, SystemErrorException, UserErrorException


class DownloadDataUserError(UserErrorException):
    def __init__(self, message):
        super().__init__(message, target=ErrorTarget.RUNTIME)


class DownloadDataSystemError(SystemErrorException):
    def __init__(self, message):
        super().__init__(message, target=ErrorTarget.RUNTIME)


class FindUnsafeFilePath(SystemErrorException):
    def __init__(self, message):
        super().__init__(message, target=ErrorTarget.RUNTIME)


def download_fileshare_data(uri: str, destination: str, datastore: Datastore) -> str:
    """
    Download data from fileshare
    """

    parsed_uri = AzureMLDatastorePathUri(uri)
    client = ShareDirectoryClient(
        account_url=_get_account_url(datastore),
        credential=_get_datastore_token(datastore),
        share_name=datastore.file_share_name,
        directory_path=parsed_uri.path,
    )
    # file share has no client to do common access for file and directory
    # dir_client's exists method will return False if the path is a file
    if client.exists():
        recursive_download(client, destination, max_concurrency=4)
        return destination

    # if dir doesn't exist, try to download file
    return _download_fileshare_file(uri, destination, datastore)


def _download_fileshare_file(uri: str, destination: str, datastore: Datastore) -> str:
    parsed_uri = AzureMLDatastorePathUri(uri)
    client = ShareFileClient(
        account_url=_get_account_url(datastore),
        credential=_get_datastore_token(datastore),
        file_path=parsed_uri.path,
        share_name=datastore.file_share_name,
    )

    target_file_name = get_target_file_path(uri, destination)
    if destination is not None and not target_file_name.startswith(os.path.normpath(destination)):
        raise FindUnsafeFilePath("It is not allowed to access a unsafe file path.")
    with open(target_file_name, "wb") as target:
        file_data = client.download_file()
        file_data.readinto(target)

    # For file, we return the input dst (parent dir path) as destination
    # This is to keep the same behavior as blob
    return destination


def get_target_file_path(uri: str, destination: str) -> str:
    """
    Get target file
    """
    target_file = _get_last_part_of_uri(uri)
    if destination is not None:
        target_file = os.path.join(destination, target_file)
    # Verify with normalized version of path
    return os.path.normpath(target_file)


def _get_last_part_of_uri(uri: str) -> str:
    """Get last part of uri"""
    return uri.split("/")[-1]


def _get_datastore_token(datastore: Datastore) -> str:
    credential = datastore.credentials
    if isinstance(credential, AccountKeyConfiguration):
        return credential.account_key
    elif hasattr(credential, "sas_token"):
        return credential.sas_token
    raise DownloadDataUserError("Cannot get datastore credential for fileshare data")


def _get_account_url(datastore: Datastore) -> str:
    storage_endpoint = _get_storage_endpoint_from_metadata()
    return STORAGE_ACCOUNT_URLS[datastore.type].format(datastore.account_name, storage_endpoint)
