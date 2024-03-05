# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from __future__ import annotations

import json
from typing import Dict

import requests
from azure.core.exceptions import ClientAuthenticationError

from promptflow.contracts.run_info import Status
from promptflow.exceptions import ErrorTarget, SystemErrorException, UserErrorException
from promptflow.runtime._errors import UserAuthenticationError
from promptflow.runtime.storage.run_storage import RuntimeAuthErrorType
from promptflow.runtime.utils import logger
from promptflow.runtime.utils._utils import get_resource_management_scope
from promptflow.runtime.utils.retry_utils import retry

PATCH_RUN_URL = (
    "{endpoint}/history/v1.0/subscriptions/{sub}/resourceGroups/{rg}/"
    "providers/Microsoft.MachineLearningServices/workspaces/{ws}/runs/{run_id}"
)
UPDATE_RUN_URL = (
    "{endpoint}/history/v1.0/subscriptions/{sub}/resourceGroups/{rg}/"
    "providers/Microsoft.MachineLearningServices/workspaces/{ws}/runs/{run_id}/events"
)
GET_RUN_URL = (
    "{endpoint}/history/v1.0/subscriptions/{sub}/resourceGroups/{rg}/"
    "providers/Microsoft.MachineLearningServices/workspaces/{ws}/runs/{run_id}"
)
GET_RUN_DETAILS_URL = (
    "{endpoint}/history/v1.0/subscriptions/{sub}/resourceGroups/{rg}/"
    "providers/Microsoft.MachineLearningServices/workspaces/{ws}/runs/{run_id}/details"
)


class RunNotFoundError(UserErrorException):
    def __init__(self, message):
        super().__init__(message, target=ErrorTarget.RUNTIME)


class RunHistorySystemError(SystemErrorException):
    def __init__(self, message):
        super().__init__(message, target=ErrorTarget.RUNTIME)


class OutputAssetInfo:
    def __init__(self, asset_id, data_type="UriFolder"):
        self.asset_id = asset_id
        self.data_type = data_type


class RunHistoryClient:
    def __init__(
        self,
        subscription_id,
        resource_group,
        workspace_name,
        service_endpoint,
        credential=None,
        runtime_config=None,
    ):
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace_name = workspace_name
        self.service_endpoint = service_endpoint
        self.credential = credential
        self.runtime_config = runtime_config

    @retry(RunHistorySystemError, tries=10, logger=logger)
    def patch_run(self, run_id, output_asset_infos: Dict[str, OutputAssetInfo]):
        try:
            patch_url = PATCH_RUN_URL.format(
                endpoint=self.service_endpoint,
                sub=self.subscription_id,
                rg=self.resource_group,
                ws=self.workspace_name,
                run_id=run_id,
            )

            logger.info(f"Patching {run_id}...")
            token = self.credential.get_token(get_resource_management_scope())
            headers = {"Authorization": "Bearer %s" % (token.token)}

            payload = {
                "Outputs": {k: {"assetId": v.asset_id, "type": v.data_type} for k, v in output_asset_infos.items()}
            }

            response = requests.patch(patch_url, headers=headers, json=payload)

            if response.status_code != 200:
                logger.error(
                    "Failed to patch Run %s. Code=%s. Message={customer_content}",
                    run_id,
                    response.status_code,
                    extra={"customer_content": response.text},
                )
            if response.status_code == 404:
                raise RunNotFoundError(response.text)
            elif response.status_code == 401 or response.status_code == 403:
                if self.runtime_config:
                    auth_error_message = self.runtime_config._get_auth_error_message(RuntimeAuthErrorType.WORKSPACE)
                else:
                    auth_error_message = response.text
                # if it's auth issue, return auth_error_message
                raise UserAuthenticationError(message=auth_error_message, target=ErrorTarget.RUNTIME)
            elif response.status_code != 200:
                raise Exception(
                    "Failed to patch Run {}. Code={}. Message={}".format(run_id, response.status_code, response.text)
                )
        except UserErrorException:
            logger.exception("Patch Run %s failed with user error.", run_id)
            raise
        except Exception as ex:
            logger.error(
                "Patch Run %s failed. exception={customer_content}",
                run_id,
                extra={"customer_content": ex},
                exc_info=True,
            )
            raise RunHistorySystemError(f"Failed to patch Run {run_id}: {str(ex)}") from ex

    @retry(RunHistorySystemError, tries=10, logger=logger)
    def update_run_status(self, run_id, run_status: Status):
        try:
            update_url = UPDATE_RUN_URL.format(
                endpoint=self.service_endpoint,
                sub=self.subscription_id,
                rg=self.resource_group,
                ws=self.workspace_name,
                run_id=run_id,
            )

            logger.info(f"Updating {run_id} to {run_status}...")
            token = self.credential.get_token(get_resource_management_scope())
            headers = {"Authorization": "Bearer %s" % (token.token)}

            payload = {
                "Name": "Microsoft.MachineLearning.Run.%s" % run_status.value,
                "Data": {
                    "RunId": run_id,
                    "Version": "1.0",
                },
            }

            response = requests.post(update_url, headers=headers, json=payload)

            if response.status_code != 200:
                logger.error(
                    "Failed to update Run %s. Code=%s. Message={customer_content}",
                    run_id,
                    response.status_code,
                    extra={"customer_content": response.text},
                )
            if response.status_code == 404:
                raise RunNotFoundError(response.text)
            elif response.status_code == 401 or response.status_code == 403:
                if self.runtime_config:
                    auth_error_message = self.runtime_config._get_auth_error_message(RuntimeAuthErrorType.WORKSPACE)
                else:
                    auth_error_message = response.text
                # if it's auth issue, return auth_error_message
                raise UserAuthenticationError(message=auth_error_message, target=ErrorTarget.RUNTIME)
            elif response.status_code != 200:
                raise Exception(
                    "Failed to update Run {}. Code={}. Message={}".format(run_id, response.status_code, response.text)
                )
        except UserErrorException:
            logger.exception("Update Run %s failed with user error.", run_id)
            raise
        except Exception as ex:
            logger.error(
                "Update Run %s failed. exception={customer_content}",
                run_id,
                extra={"customer_content": ex},
                exc_info=True,
            )
            raise RunHistorySystemError(f"Failed to update Run {run_id}: {str(ex)}") from ex

    @retry(RunHistorySystemError, tries=10, logger=logger)
    @retry(ClientAuthenticationError, tries=3, logger=logger)
    def get_run(self, run_id):
        try:
            get_url = GET_RUN_URL.format(
                endpoint=self.service_endpoint,
                sub=self.subscription_id,
                rg=self.resource_group,
                ws=self.workspace_name,
                run_id=run_id,
            )

            token = self.credential.get_token(get_resource_management_scope())
            headers = {"Authorization": "Bearer %s" % (token.token)}

            response = requests.get(get_url, headers=headers)

            if response.status_code != 200:
                logger.error(
                    "Failed to Get Run %s. Code=%s. Message={customer_content}",
                    run_id,
                    response.status_code,
                    extra={"customer_content": response.text},
                )
            if response.status_code == 404:
                raise RunNotFoundError(response.text)
            elif response.status_code == 401 or response.status_code == 403:
                if self.runtime_config:
                    auth_error_message = self.runtime_config._get_auth_error_message(RuntimeAuthErrorType.WORKSPACE)
                else:
                    auth_error_message = response.text
                # if it's auth issue, return auth_error_message
                raise UserAuthenticationError(message=auth_error_message, target=ErrorTarget.RUNTIME)
            elif response.status_code != 200:
                raise Exception(
                    "Failed to get Run {}. Code={}. Message={}".format(run_id, response.status_code, response.text)
                )
            return json.loads(response.content)
        except ClientAuthenticationError as ex:
            logger.error(
                "Get Run %s failed. exception={customer_content}",
                run_id,
                extra={"customer_content": ex},
                exc_info=True,
            )
            raise
        except UserErrorException:
            logger.exception("Get Run %s failed with user error.", run_id)
            raise
        except Exception as ex:
            logger.error(
                "Get Run %s failed. exception={customer_content}",
                run_id,
                extra={"customer_content": ex},
                exc_info=True,
            )
            raise RunHistorySystemError(f"Failed to get Run {run_id}: {str(ex)}") from ex

    @retry(RunHistorySystemError, tries=10, logger=logger)
    @retry(ClientAuthenticationError, tries=3, logger=logger)
    def get_run_details(self, run_id):
        try:
            get_url = GET_RUN_DETAILS_URL.format(
                endpoint=self.service_endpoint,
                sub=self.subscription_id,
                rg=self.resource_group,
                ws=self.workspace_name,
                run_id=run_id,
            )

            token = self.credential.get_token(get_resource_management_scope())
            headers = {"Authorization": "Bearer %s" % (token.token)}

            response = requests.get(get_url, headers=headers)

            if response.status_code != 200:
                logger.error(
                    "Failed to Get Run Details %s. Code=%s. Message={customer_content}",
                    run_id,
                    response.status_code,
                    extra={"customer_content": response.text},
                )
            if response.status_code == 404:
                raise RunNotFoundError(response.text)
            elif response.status_code == 401 or response.status_code == 403:
                if self.runtime_config:
                    auth_error_message = self.runtime_config._get_auth_error_message(RuntimeAuthErrorType.WORKSPACE)
                else:
                    auth_error_message = response.text
                # if it's auth issue, return auth_error_message
                raise UserAuthenticationError(message=auth_error_message, target=ErrorTarget.RUNTIME)
            elif response.status_code != 200:
                raise Exception(
                    "Failed to get Run details {}. Code={}. Message={}".format(
                        run_id, response.status_code, response.text
                    )
                )
            return json.loads(response.content)
        except ClientAuthenticationError as ex:
            logger.error(
                "Get Run Details %s failed. exception={customer_content}",
                run_id,
                extra={"customer_content": ex},
                exc_info=True,
            )
            raise
        except UserErrorException:
            logger.exception("Get Run Details %s failed with user error.", run_id)
            raise
        except Exception as ex:
            logger.error(
                "Get Run Details %s failed. exception={customer_content}",
                run_id,
                extra={"customer_content": ex},
                exc_info=True,
            )
            raise RunHistorySystemError(f"Failed to get Run details {run_id}: {str(ex)}") from ex
