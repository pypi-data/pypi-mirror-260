# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from concurrent.futures import ThreadPoolExecutor, wait
from pathlib import Path

import requests
from azure.storage.blob import BlobClient

from promptflow.exceptions import UserErrorException
from promptflow.runtime._errors import (
    DownloadSnapshotFailed,
    GetSnapshotSasUrlFailed,
    NoSpaceLeftOnDevice,
    SnapshotNotFound,
    UserAuthenticationError,
)
from promptflow.runtime.runtime_config import RuntimeConfig
from promptflow.runtime.storage.run_storage import RuntimeAuthErrorType
from promptflow.runtime.utils import logger
from promptflow.runtime.utils._token_utils import get_default_credential
from promptflow.runtime.utils._utils import get_resource_management_scope
from promptflow.runtime.utils.retry_utils import retry

SNAPSHOT_SAS_URL = (
    "{endpoint}/content/v2.0/subscriptions/{sub}/resourceGroups/{rg}/"
    "providers/Microsoft.MachineLearningServices/workspaces/{ws}/snapshots/sas"
)
PARALLEL_DOWNLOADING_TASK = 10


class SnapshotsClient:
    def __init__(self, runtime_config: RuntimeConfig):
        self.credential = get_default_credential()
        self.subscription_id = runtime_config.deployment.subscription_id
        self.resource_group = runtime_config.deployment.resource_group
        self.workspace_name = runtime_config.deployment.workspace_name
        self.service_endpoint = runtime_config.deployment.mt_service_endpoint
        self.runtime_config = runtime_config

    @retry(DownloadSnapshotFailed, tries=3, logger=logger)
    def download_snapshot(self, snapshot_id: str, target_path: Path):
        try:
            self.download_snapshot_with_threads(snapshot_id, target_path)
        except UserErrorException:
            logger.exception("Download snapshot %s failed with user error.", snapshot_id)
            raise
        except Exception as ex:
            logger.error(
                f"Download snapshot {snapshot_id} failed. Exception: {{customer_content}}",
                exc_info=True,
                extra={"customer_content": str(ex)},
            )
            if "No space left on device" in str(ex):
                raise NoSpaceLeftOnDevice(str(ex))
            raise DownloadSnapshotFailed(
                message_format="Failed to download snapshot {snapshot_id}: {exception_message}",
                snapshot_id=snapshot_id,
                exception_message=str(ex),
            ) from ex

    def download_snapshot_with_threads(self, snapshot_id: str, target_path: Path):
        snapshot_sas_url = SNAPSHOT_SAS_URL.format(
            endpoint=self.service_endpoint,
            sub=self.subscription_id,
            rg=self.resource_group,
            ws=self.workspace_name,
        )
        logger.info(f"Get snapshot sas url for {snapshot_id}.")
        token = self.credential.get_token(get_resource_management_scope())
        headers = {"Authorization": "Bearer %s" % (token.token)}
        body = {"snapshotOrAssetId": snapshot_id}
        response = requests.post(snapshot_sas_url, headers=headers, json=body)
        if response.status_code == 200:
            snapshot_meta = response.json()

            all_files = {}
            traverse_snapshot_children(snapshot_meta, "", all_files)
            logger.info(f"Snapshot {snapshot_id} contains {len(all_files)} files.")

            with ThreadPoolExecutor(max_workers=PARALLEL_DOWNLOADING_TASK) as executor:
                futures = []
                for file, sas_url in all_files.items():
                    futures.append(executor.submit(download_blob_with_sas_url, sas_url, target_path / file))
                done, _ = wait(futures)
                for future in done:
                    # propagate exception if any
                    future.result()

            logger.info(f"Download snapshot {snapshot_id} completed.")
        elif response.status_code == 404:
            raise SnapshotNotFound(message=response.text)
        elif response.status_code == 401 or response.status_code == 403:
            auth_error_message = self.runtime_config._get_auth_error_message(RuntimeAuthErrorType.WORKSPACE)
            # if it's auth issue, return auth_error_message
            raise UserAuthenticationError(message=auth_error_message)
        elif response.status_code != 200:
            raise GetSnapshotSasUrlFailed(
                message_format="Failed to get snapshot sas url for {snapshot_id}. Code={status_code}. Message={msg}",
                snapshot_id=snapshot_id,
                status_code=response.status_code,
                msg=response.text,
            )


def traverse_snapshot_children(snapshot_meta: dict, path_prefix: str, all_files: dict):
    """Recursively traverse the snapshot children and collect all files with sasUrl."""
    for name, meta in snapshot_meta["children"].items():
        if meta["type"].lower() == "file":
            all_files[path_prefix + name] = meta["sasUrl"]
        elif meta["type"].lower() == "directory":
            traverse_snapshot_children(meta, path_prefix + name + "/", all_files)


def download_blob_with_sas_url(blob_sas_url: str, local_path: Path):
    """Download blob with sas url to local path."""
    Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    blob_client = BlobClient.from_blob_url(blob_sas_url)
    with open(local_path, "wb") as f:
        f.write(blob_client.download_blob().readall())
