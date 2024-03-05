from promptflow._internal import GenerateMetaUserError
from promptflow.exceptions import ErrorTarget, SystemErrorException, UserErrorException, ValidationException

# region runtime.runtime_config


class InvalidClientAuthentication(UserErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class UserAuthenticationValidationError(UserErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class MissingDeploymentConfigs(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class ConfigFileNotExists(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class InvalidRunStorageType(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


# endregion


# region runtime.runtime


class UnexpectedOutputSubDir(UserErrorException):
    """Exception raised when user authentication failed"""

    pass


class UserAuthenticationError(UserErrorException):
    """Exception raised when user authentication failed"""

    pass


class FlowRunTimeoutError(UserErrorException):
    """Exception raised when sync submission flow run timeout"""

    def __init__(self, timeout):
        super().__init__(message=f"Flow run timeout for exceeding {timeout} seconds", target=ErrorTarget.RUNTIME)


class UnexpectedFlowSourceType(UserErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class InvalidDataInputs(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class DataInputsNotfound(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class InvalidAssetId(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


# endregion


# region runtime.data


class RuntimeConfigNotProvided(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class InvalidDataUri(UserErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class InvalidAmlDataUri(InvalidDataUri):
    pass


class InvalidBlobDataUri(InvalidDataUri):
    pass


class InvalidWasbsDataUri(InvalidDataUri):
    pass


class InvalidRegistryDataUri(InvalidDataUri):
    pass


# endregion


# region runtime.connection


class ConnectionNotSet(ValidationException):
    pass


class ResolveConnectionForFlowError(ValidationException):
    pass


class AccessDeniedError(UserErrorException):
    """Exception raised when run info can not be found in storage"""

    def __init__(self, operation: str, target: ErrorTarget):
        super().__init__(message=f"Access is denied to perform operation {operation!r}", target=target)


class OpenURLFailed(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class OpenURLUserAuthenticationError(UserAuthenticationError):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class OpenURLFailedUserError(UserErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class OpenURLNotFoundError(OpenURLFailedUserError):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UnknownConnectionType(UserErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class ConnectionDataInvalidError(UserErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


# endregion


# region runtime._utils._snapshots_client


class SnapshotNotFound(UserErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class NoSpaceLeftOnDevice(UserErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class InvalidFlowYaml(UserErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class GetSnapshotSasUrlFailed(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class DownloadSnapshotFailed(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


# endregion


# region runtime._utils._flow_source_helper


class AzureFileShareAuthenticationError(UserAuthenticationError):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class AzureFileShareNotFoundError(UserErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class AzureFileShareSystemError(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


# endregion


# region runtime.app


class GenerateMetaTimeout(GenerateMetaUserError):
    pass


class GenerateMetaSystemError(SystemErrorException):
    """Base exception raised when failed to validate tool."""

    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


class NoToolTypeDefined(GenerateMetaSystemError):
    pass


class RuntimeTerminatedByUser(UserErrorException):
    def __init__(self, message):
        super().__init__(message, target=ErrorTarget.RUNTIME)


class FlowFileNotFound(UserErrorException):
    pass


class NodeVariantInfoInvalid(SystemErrorException):
    def __init__(self, message):
        super().__init__(message=message, target=ErrorTarget.RUNTIME)


class AzureStorageSettingMissing(SystemErrorException):
    def __init__(self, message):
        super().__init__(message=message, target=ErrorTarget.RUNTIME)


# endregion


# region _utils.run_result_parser


class RunResultParseError(SystemErrorException):
    """Exception raised when failed to parse run result.

    We parse the run result to extract the run error.
    The error message is then populated in the response body.

    This exception is a SystemError since the extraction should always succeed.
    """

    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)

    @property
    def message_format(self):
        return "Failed to parse run result: {error_type_and_message}"

    @property
    def message_parameters(self):
        error_type_and_message = None
        if self.inner_exception:
            error_type_and_message = f"({self.inner_exception.__class__.__name__}) {self.inner_exception}"

        return {
            "error_type_and_message": error_type_and_message,
        }


# endregion


# region runtime.data


class StorageAuthenticationError(UserAuthenticationError):
    """Exception raised when storage authentication failed"""

    pass


class RunStorageError(SystemErrorException):
    """Exception raised for error in storage"""

    def __init__(self, message, target: ErrorTarget, storage_type: type):
        msg = f"Error of {storage_type.__qualname__!r}: {message}."
        super().__init__(message=msg, target=target)


class RunInfoNotFoundInStorageError(RunStorageError):
    """Exception raised when run info can not be found in storage"""

    def __init__(self, message: str, target: ErrorTarget, storage_type: type):
        super().__init__(message=message, target=target, storage_type=storage_type)


class AzureStorageUserError(UserErrorException):
    """Exception raised when Azure storage operation failed."""

    pass


class AzureStorageOperationError(SystemErrorException):
    """Exception raised when Azure storage operation failed."""

    pass


class AzureStoragePackagesNotInstalledError(ValidationException):
    pass


class TableAuthenticationError(UserAuthenticationError):
    pass


class BlobAuthenticationError(UserAuthenticationError):
    pass


class AmlRunStorageInitError(SystemErrorException):
    """Exception raised when import package failed."""

    def __init__(self, message: str, target: ErrorTarget = ErrorTarget.AZURE_RUN_STORAGE):
        super().__init__(message=message, target=target)


class CredentialMissing(AmlRunStorageInitError):
    pass


class MLClientMissing(AmlRunStorageInitError):
    pass


class TableInitResponseError(AzureStorageOperationError):
    pass


class BlobInitResponseError(AzureStorageOperationError):
    pass


class TableStorageInitError(AzureStorageOperationError):
    pass


class RetriableTableStorageError(AzureStorageOperationError):
    pass


class BlobStorageInitError(AzureStorageOperationError):
    pass


class RunNotFoundInTable(AzureStorageOperationError):
    pass


class CannotCreateExistingRunInTable(AzureStorageOperationError):
    pass


class CannotCreateExistingRunInBlob(AzureStorageOperationError):
    pass


class TableStorageWriteError(AzureStorageOperationError):
    pass


class StorageWriteForbidden(UserAuthenticationError):
    pass


class StorageHttpResponseError(AzureStorageOperationError):
    pass


class BlobStorageWriteError(AzureStorageOperationError):
    pass


class FailedToConvertRecordToRunInfo(AzureStorageOperationError):
    pass


class GetFlowRunError(RunInfoNotFoundInStorageError):
    pass


class GetFlowRunResponseError(RunInfoNotFoundInStorageError):
    pass


class FlowIdMissing(ValidationException):
    pass


class UnsupportedRunInfoTypeInBlob(ValidationException):
    pass


class MLFlowOperationError(SystemErrorException):
    """Exception raised when mlflow helper operation failed."""

    def __init__(self, message: str, target: ErrorTarget = ErrorTarget.AZURE_RUN_STORAGE):
        super().__init__(message=message, target=target)


class InvalidMLFlowTrackingUri(ValidationException):
    pass


class FailedToStartRun(MLFlowOperationError):
    pass


class FailedToStartRunAfterCreated(MLFlowOperationError):
    pass


class FailedToCreateRun(MLFlowOperationError):
    pass


class FailedToEndRootRun(MLFlowOperationError):
    pass


class FailedToCancelWithAnotherActiveRun(MLFlowOperationError):
    pass


class FailedToCancelRun(MLFlowOperationError):
    pass


class CannotEndRunWithNonTerminatedStatus(MLFlowOperationError):
    pass


class FailedToGetHostCreds(MLFlowOperationError):
    pass


class RunStorageConfigMissing(ValidationException):
    pass


class PartitionKeyMissingForRunQuery(ValidationException):
    pass


class BuildConnectionSystemError(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)


# endregion


# region helper methods


def to_string(ex: Exception) -> str:
    return f"{type(ex).__name__}: {str(ex)}"


def get_status_code(exception):
    """
    Get the status code from an exception if available.

    Parameters:
        exception: The exception object from which to extract the status code.

    Returns:
        The status code if available, or None if not present.
    """
    if hasattr(exception, "status_code"):
        return exception.status_code
    elif hasattr(exception, "response") and hasattr(exception.response, "status_code"):
        return exception.response.status_code
    else:
        return None


def get_exception_type(exception):
    """Get the type of an exception."""
    return type(exception).__name__


def get_error_code(exception):
    """
    Extracts the error code from an exception if available.
    Returns None if the error code is not present.
    """
    return getattr(exception, "error_code", None)


# endregion
