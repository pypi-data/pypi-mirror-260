import os
import re
import subprocess
from pathlib import Path

from promptflow._internal import CredentialScrubber
from promptflow.runtime._errors import (
    AzureFileShareAuthenticationError,
    AzureFileShareNotFoundError,
    AzureFileShareSystemError,
)
from promptflow.runtime.constants import ComputeType
from promptflow.runtime.contracts.runtime import AzureFileShareInfo
from promptflow.runtime.utils.retry_utils import retry

from . import logger

AZCOPY_EXE = os.environ.get("AZCOPY_EXECUTABLE", "azcopy")
CI_MOUNTED_ROOT = "/mnt/cloud/code"

ERROR_CODE_PATTERN = re.compile(r"Code: (.*?)\n")
ERROR_DESCRIPTION_PATTERN = re.compile(r"Description=(.*?)\n")
EXCLUDE_PATHS = ".runs;.promptflow"


def fill_working_dir(
    compute_type: ComputeType, flow_source_info: AzureFileShareInfo, run_id: str, flow_dag_file: str = None
):
    working_dir = flow_source_info.working_dir
    runtime_dir = working_dir
    if compute_type == ComputeType.COMPUTE_INSTANCE:
        runtime_dir = os.path.join(CI_MOUNTED_ROOT, working_dir)
    elif compute_type == ComputeType.MANAGED_ONLINE_DEPLOYMENT:
        runtime_dir = Path("requests", run_id).resolve()
        os.makedirs(runtime_dir, exist_ok=True)
        sas_url = flow_source_info.sas_url
        logger.info("Download azure file share for run %s start", run_id)
        _download_azure_file_share(sas_url, runtime_dir, run_id, True, EXCLUDE_PATHS)

        # flow_dag_file may under .runs folder that excluded. Should download it and exclude other .runs folder
        # For example, flow_dag_file may specify as ".runs/dd945e4d-37f1-4e50-9bd0-cdd034e4407d/flow.dag.yaml"
        if flow_dag_file is not None:
            flow_dag_file_url = sas_url.replace("*", flow_dag_file)
            flow_dag_file_runtime_path = os.path.join(runtime_dir, flow_dag_file)
            _download_azure_file_share(flow_dag_file_url, flow_dag_file_runtime_path, run_id, False)
        logger.info("Download azure file share for run %s finished", run_id)

    return runtime_dir


@retry(AzureFileShareSystemError, tries=3, logger=logger)
def _download_azure_file_share(sas_url, runtime_path, run_id, recursive, exclude_path=None):
    cmd = '%s copy "%s" "%s"' % (AZCOPY_EXE, sas_url, runtime_path)
    if recursive:
        cmd += " --recursive"
    if exclude_path is not None:
        cmd += ' --exclude-path "%s"' % exclude_path
    logger.info("cmd: %s", cmd)
    file_share_url = sas_url[: sas_url.find("?")]
    logger.info(
        "Start azcopy copy the sasurl. file share url: {customer_content}. runtime_path: %s",
        runtime_path,
        extra={"customer_content": file_share_url},
    )
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    credential_scrubber = CredentialScrubber()
    stdout = credential_scrubber.scrub(stdout.decode())
    stderr = credential_scrubber.scrub(stderr.decode())

    if p.returncode != 0:
        logger.info("Azcopy for run %s stdout: {customer_content}", run_id, extra={"customer_content": stdout})
        if len(stderr) > 0:
            logger.error("Azcopy for run %s stderr: {customer_content}", run_id, extra={"customer_content": stderr})
        logger.error("Azcopy failed to download for run %s. Return code: %s", run_id, p.returncode)
        error_message = "\n".join([stdout, stderr])
        _handle_azcopy_error_messages(error_message)


def _handle_azcopy_error_messages(error_message):
    error_code_line = ERROR_CODE_PATTERN.search(error_message)
    if error_code_line is not None:
        error_code = error_code_line.group(1)
        description_line = ERROR_DESCRIPTION_PATTERN.search(error_message)
        if description_line is not None:
            description = description_line.group(1)
        else:
            description = error_code
        message_format = "Download azure file share failed. Code: {error_code}. Description: {description}"
        logger.error(f"Download azure file share failed. Code: {error_code}.")
        if error_code in ["AuthenticationFailed", "AuthorizationPermissionMismatch"]:
            raise AzureFileShareAuthenticationError(
                message_format=message_format, error_code=error_code, description=description
            )
        elif error_code == "ResourceNotFound":
            raise AzureFileShareNotFoundError(
                message_format=message_format, error_code=error_code, description=description
            )
        else:
            raise AzureFileShareSystemError(
                message_format=message_format, error_code=error_code, description=description
            )
    raise AzureFileShareSystemError(message=error_message)
