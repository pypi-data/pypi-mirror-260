import os
import threading
from pathlib import Path
from typing import Optional

from docker.models.containers import Container

from promptflow.runtime.executor_image_manager import (
    EXECUTOR_CONTAINER_PORT,
    HOST_MOUNT_PATH,
    WORKING_DIR_IN_CONTAINER,
    executor_image_manager,
)
from promptflow.runtime.utils import logger
from promptflow.runtime.utils.internal_logger_utils import BlobStream
from promptflow.storage._run_storage import AbstractRunStorage

INIT_ERROR_FILE_NAME = "init_error.json"


try:
    from promptflow._internal import CSharpBaseExecutorProxy
except ImportError:

    class CSharpBaseExecutorProxy:
        def __init__(self, *args, **kwargs):
            raise Exception(
                (
                    "CSharpBaseExecutorProxy is not found in promptflow._internal. "
                    "Please install promptflow>=1.5.0 to submit c# batch run."
                )
            )


def _get_connection_endpoint() -> str:
    # Endpoint of runtime server.
    port = os.environ.get("PORT", 8080)
    return f"http://{os.environ.get('HOSTNAME')}:{port}/v1.0"


def _get_entrypoint():
    connection_endpoint = _get_connection_endpoint()
    init_error_file_path = Path(WORKING_DIR_IN_CONTAINER) / INIT_ERROR_FILE_NAME
    # Change to container working dir and start service.
    command_to_start_service = (
        f"cd {WORKING_DIR_IN_CONTAINER} && "
        f"dotnet Promptflow.dll --execution_service --port {EXECUTOR_CONTAINER_PORT} --yaml_path flow.dag.yaml --connection_provider_url {connection_endpoint} --log_level Warning --error_file_path {init_error_file_path}"  # noqa: E501
    )
    return ["sh", "-c", command_to_start_service]


def _collect_logs(container: Container, sas_uri: str):
    blob_stream = BlobStream(sas_uri, raise_exception=False)
    for log in container.logs(stream=True, follow=True):
        log_str = log.decode("utf-8")
        # No need to add try/catch here because no exception will be raised.
        blob_stream.write(log_str)


def _kill_container_without_exception(container_name):
    try:
        executor_image_manager.kill_container(container_name)
    except Exception as ex:
        logger.warning(f"Failed to kill container {container_name}. Exception: {ex}")


class CSharpExecutorProxy(CSharpBaseExecutorProxy):
    def __init__(self, container: Container, working_dir: Optional[Path] = None):
        self._container = container
        super().__init__(working_dir=working_dir)

    @property
    def api_endpoint(self) -> str:
        return f"http://{self._container.name}:{EXECUTOR_CONTAINER_PORT}"

    @classmethod
    async def create(
        cls,
        flow_file: Path,
        working_dir: Optional[Path],
        connections: Optional[dict],
        storage: Optional[AbstractRunStorage],
        container_name: str,
        log_path: str,
        **kwargs,
    ) -> "CSharpExecutorProxy":
        executor_image_manager.init()
        entrypoint = _get_entrypoint()
        working_dir_in_host = str(working_dir).replace(HOST_MOUNT_PATH, "")
        try:
            container: Container = executor_image_manager.run_container(
                lang="csharp",
                container_name=container_name,
                entrypoint=entrypoint,
                mounts=[(working_dir_in_host, WORKING_DIR_IN_CONTAINER)],
            )

            # Starting a daemon thread to collect log.
            logger.info("Starting a daemon thread to collect executor container log...")
            log_thread = threading.Thread(target=_collect_logs, args=(container, log_path))
            log_thread.daemon = True
            log_thread.start()
        except Exception as ex:
            logger.error(f"Failed to start container {container_name}. Exception: {ex}")
            logger.warning(f"Killing container {container_name}...")
            _kill_container_without_exception(container_name)
            raise ex
        executor_proxy = CSharpExecutorProxy(container, Path(working_dir))
        init_error_file_path = Path(working_dir) / INIT_ERROR_FILE_NAME
        init_error_file_path.touch()
        await executor_proxy.ensure_executor_startup(init_error_file_path)
        return executor_proxy

    async def destroy(self):
        _kill_container_without_exception(self._container.name)
