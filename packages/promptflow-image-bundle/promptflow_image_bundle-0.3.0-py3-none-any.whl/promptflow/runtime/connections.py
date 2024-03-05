import os
from enum import Enum
from typing import Any, Union

import requests
from azure.core.exceptions import ClientAuthenticationError

from promptflow._internal import (
    get_used_connection_names_from_environment_variables,
    update_environment_variables_with_connections,
)
from promptflow.connections import CustomConnection

# TODO: Move to azure.ai.ml._restclient...models after new type ApiKey, CustomKeys added.
from promptflow.exceptions import ErrorTarget
from promptflow.runtime._errors import BuildConnectionSystemError, UserErrorException
from promptflow.runtime.constants import ENV_AZURE_RESOURCE_MANAGER
from promptflow.runtime.utils import logger
from promptflow.runtime.utils._token_utils import get_default_credential
from promptflow.runtime.utils._utils import get_resource_management_scope
from promptflow.runtime.utils.retry_utils import retry

from ._errors import (
    AccessDeniedError,
    OpenURLFailed,
    OpenURLFailedUserError,
    OpenURLNotFoundError,
    OpenURLUserAuthenticationError,
    UnknownConnectionType,
)

GET_CONNECTION_URL = (
    "/subscriptions/{sub}/resourcegroups/{rg}/providers/Microsoft.MachineLearningServices"
    "/workspaces/{ws}/connections/{name}/listsecrets?api-version=2023-04-01-preview"
)
LIST_CONNECTION_URL = (
    "/subscriptions/{sub}/resourcegroups/{rg}/providers/Microsoft.MachineLearningServices"
    "/workspaces/{ws}/connections?api-version=2023-04-01-preview"
)
FLOW_META_PREFIX = "azureml.flow."


class ConnectionCategory(str, Enum):
    AzureOpenAI = "AzureOpenAI"
    CognitiveSearch = "CognitiveSearch"
    CognitiveService = "CognitiveService"
    CustomKeys = "CustomKeys"


def open_url(token, url, action, method="GET", model=None) -> Union[Any, dict]:
    """
    :type token: str
    :type url: str
    :type action: str, for the error message format.
    :type method: str
    :type model: Type[msrest.serialization.Model]
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.request(method, url, headers=headers)
    message_format = (
        f"Open url {{url}} failed with status code: {response.status_code}, action: {action}, reason: {{reason}}"
    )
    if response.status_code == 403:
        raise AccessDeniedError(operation=url, target=ErrorTarget.RUNTIME)
    elif response.status_code == 404:
        raise OpenURLNotFoundError(
            message_format=message_format,
            url=url,
            reason=response.reason,
        )
    elif 400 <= response.status_code < 500:
        raise OpenURLFailedUserError(
            message_format=message_format,
            url=url,
            reason=response.reason,
        )
    elif response.status_code != 200:
        raise OpenURLFailed(
            message_format=message_format,
            url=url,
            reason=response.reason,
        )
    data = response.json()
    if model:
        return model.deserialize(data)
    return data


def validate_and_fallback_connection_type(name, type_name, category, metadata):
    if type_name:
        return type_name
    if category == ConnectionCategory.AzureOpenAI:
        return "AzureOpenAI"
    if category == ConnectionCategory.CognitiveSearch:
        return "CognitiveSearch"
    if category == ConnectionCategory.CognitiveService:
        kind = get_case_insensitive_key(metadata, "Kind")
        if kind == "Content Safety":
            return "AzureContentSafety"
        if kind == "Form Recognizer":
            return "FormRecognizer"
    raise UnknownConnectionType(
        message_format="Connection {name} is not recognized in PromptFlow, "
        "please make sure the connection is created in PromptFlow.",
        category=category,
        name=name,
    )


def get_case_insensitive_key(d, key, default=None):
    for k, v in d.items():
        if k.lower() == key.lower():
            return v
    return default


def build_connection_dict_from_rest_object(name, obj) -> dict:
    """
    :type name: str
    :type obj: promptflow.runtime.models.WorkspaceConnectionPropertiesV2BasicResource
    """
    # Reference 1: https://msdata.visualstudio.com/Vienna/_git/vienna?path=/src/azureml-api/src/AccountRP/Contracts/WorkspaceConnection/WorkspaceConnectionDtoV2.cs&_a=blame&version=GBmaster  # noqa: E501
    # Reference 2: https://msdata.visualstudio.com/Vienna/_git/vienna?path=%2Fsrc%2Fazureml-api%2Fsrc%2FDesigner%2Fsrc%2FMiddleTier%2FMiddleTier%2FServices%2FPromptFlow%2FConnectionsManagement.cs&version=GBmaster&_a=contents  # noqa: E501
    # This connection type covers the generic ApiKey auth connection categories, for examples:
    # AzureOpenAI:
    #     Category:= AzureOpenAI
    #     AuthType:= ApiKey (as type discriminator)
    #     Credentials:= {ApiKey} as <see cref="ApiKey"/>
    #     Target:= {ApiBase}
    #
    # CognitiveService:
    #     Category:= CognitiveService
    #     AuthType:= ApiKey (as type discriminator)
    #     Credentials:= {SubscriptionKey} as <see cref="ApiKey"/>
    #     Target:= ServiceRegion={serviceRegion}
    #
    # CognitiveSearch:
    #     Category:= CognitiveSearch
    #     AuthType:= ApiKey (as type discriminator)
    #     Credentials:= {Key} as <see cref="ApiKey"/>
    #     Target:= {Endpoint}
    #
    # Use Metadata property bag for ApiType, ApiVersion, Kind and other metadata fields
    properties = obj.properties
    type_name = get_case_insensitive_key(properties.metadata, f"{FLOW_META_PREFIX}connection_type")
    type_name = validate_and_fallback_connection_type(name, type_name, properties.category, properties.metadata)
    module = get_case_insensitive_key(properties.metadata, f"{FLOW_META_PREFIX}module", "promptflow.connections")
    # Note: Category is connectionType in MT, but type name should be class name, which is flowValueType in MT.
    # Handle old connections here, see details: https://github.com/Azure/promptflow/tree/main/connections
    type_name = f"{type_name}Connection" if not type_name.endswith("Connection") else type_name
    meta = {"type": type_name, "module": module}

    if properties.category == ConnectionCategory.AzureOpenAI:
        value = {
            "api_key": properties.credentials.key,
            "api_base": properties.target,
            "api_type": get_case_insensitive_key(properties.metadata, "ApiType"),
            "api_version": get_case_insensitive_key(properties.metadata, "ApiVersion"),
        }
    elif properties.category == ConnectionCategory.CognitiveSearch:
        value = {
            "api_key": properties.credentials.key,
            "api_base": properties.target,
            "api_version": get_case_insensitive_key(properties.metadata, "ApiVersion"),
        }
    elif properties.category == ConnectionCategory.CognitiveService:
        value = {
            "api_key": properties.credentials.key,
            "endpoint": properties.target,
            "api_version": get_case_insensitive_key(properties.metadata, "ApiVersion"),
        }
    elif properties.category == ConnectionCategory.CustomKeys:
        # Merge secrets from credentials.keys and other string fields from metadata
        value = {
            **properties.credentials.keys,
            **{k: v for k, v in properties.metadata.items() if not k.startswith(FLOW_META_PREFIX)},
        }
        if type_name == CustomConnection.__name__:
            meta["secret_keys"] = list(properties.credentials.keys.keys())
    else:
        raise UnknownConnectionType(
            message_format=(
                "Unknown connection {name} category {category}, please upgrade your promptflow sdk version and retry."
            ),
            category=properties.category,
            name=name,
        )
    # Note: Filter empty values out to ensure default values can be picked when init class object.
    return {**meta, "value": {k: v for k, v in value.items() if v}}


@retry((BuildConnectionSystemError, ClientAuthenticationError), tries=3)
def build_connection_dict(connection_names, subscription_id, resource_group, workspace_name, credential=None) -> dict:
    """
    :type connection_names: set
    :type subscription_id: str
    :type resource_group: str
    :type workspace_name: str
    :type credential: azure.core.credentials.TokenCredential
    """
    from promptflow.runtime.models import WorkspaceConnectionPropertiesV2BasicResource

    try:
        if not credential:
            credential = get_default_credential()
        connections = {}
        for name in connection_names:
            url = GET_CONNECTION_URL.format(sub=subscription_id, rg=resource_group, ws=workspace_name, name=name)
            try:
                host = os.environ.get(ENV_AZURE_RESOURCE_MANAGER, "https://management.azure.com")
                full_url = f"{host}{url}"
                rest_obj: WorkspaceConnectionPropertiesV2BasicResource = open_url(
                    credential.get_token(get_resource_management_scope()).token,
                    url=full_url,
                    action="listsecrets",
                    method="POST",
                    model=WorkspaceConnectionPropertiesV2BasicResource,
                )
            except AccessDeniedError:
                auth_error_message = (
                    "Access denied to list workspace secret due to invalid authentication. "
                    "Please assign RBAC role 'Azure Machine Learning Workspace Connection Secrets Reader' "
                    "to the endpoint for current workspace, "
                    "and wait for a few minutes to make sure the new role takes effect. "
                    "More details can be found in https://aka.ms/pf-deploy-identity."
                )
                raise OpenURLUserAuthenticationError(message=auth_error_message)
            try:
                connections[name] = build_connection_dict_from_rest_object(name, rest_obj)
            except Exception as e:
                logger.error(
                    f"Build connection dict for connection {name} failed with {{customer_content}}.",
                    extra={"customer_content": e},
                )
                # TODO: Refine this so that we could use our exception class and
                # know the root cause error at the same time.
                raise e
        return connections
    except UserErrorException:
        raise
    except ClientAuthenticationError:
        raise
    except Exception as e:
        raise BuildConnectionSystemError(message="Build connection dict failed") from e


def get_workspace_connection_names(client):
    # TODO: Change this to list from ARM api.
    """Get the connection dict from MT and construct to dict format"""
    from promptflow.azure import PFClient

    pf = PFClient(
        credential=client._credential,
        subscription_id=client.subscription_id,
        resource_group_name=client.resource_group_name,
        workspace_name=client.workspace_name,
    )
    connections = pf._connections.list()
    return {conn.name for conn in connections}


# Do not delete these, used by PRS team.
# Please make sure you have contact with PRS team before changing the interface.
get_used_connection_names_from_environment_variables = get_used_connection_names_from_environment_variables
update_environment_variables_with_connections = update_environment_variables_with_connections
