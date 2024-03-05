# TODO: delete network.


import os
import time
from typing import Dict, List, Tuple, Union

import docker
from docker.errors import NotFound
from docker.models.networks import Container, Network
from docker.types import Mount

from promptflow.runtime.utils import logger

DOCKER_SOCKET_PATH = "unix://var/run/docker.sock"
EXECUTOR_CONTAINER_PORT = 8080
HOST_MOUNT_PATH = "/mnt/host"
WORKING_DIR_IN_CONTAINER = "/flow"

language_to_default_image = {"csharp": "mcr.microsoft.com/azureml/promptflow/promptflow-dotnet:20240303.v1"}


def _get_network_name() -> str:
    return f"bridge-{os.environ.get('HOSTNAME')}"


def _check_container_in_network(container, network) -> bool:
    networks = container.attrs["NetworkSettings"]["Networks"]
    return network.name in networks


class ExecutorImageManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        """get singleton instance."""
        if cls._instance is None:
            cls._instance = ExecutorImageManager()
        return cls._instance

    def init(self):
        if getattr(self, "_initialized", False):
            return
        self._client = docker.DockerClient(base_url=DOCKER_SOCKET_PATH)
        self._wait_for_preparation_is_done()
        self._network = self.get_network()
        self._initialized = True

    def get_network(self):
        network_name = _get_network_name()
        networks = self._client.networks.list(names=[network_name])
        if len(networks) == 0:
            raise Exception(f"Failed to get network with name {network_name}")

        return networks[0]

    def run_container(
        self,
        lang: str,
        container_name: str,
        entrypoint: Union[List, str],
        mounts: List[Tuple[str]],
        environment_variables: Dict[str, str] = None,
    ) -> Container:
        if lang not in language_to_default_image:
            raise ValueError(f"Language {lang} is not supported.")

        image = language_to_default_image[lang]
        mount_list = []
        for m in mounts:
            mount_list.append(
                Mount(
                    source=m[0],
                    target=m[1],
                    type="bind",
                    read_only=False,
                )
            )
        logger.info(f"Running container {container_name} using image {image}... ")
        if environment_variables is None:
            environment_variables = dict()
        return self._client.containers.run(
            image=image,
            detach=True,
            mounts=mount_list,
            restart_policy={"Name": "on-failure", "MaximumRetryCount": 0},  # No restart. May need to be improved.
            network=self._network.name,
            name=container_name,
            entrypoint=entrypoint,
            environment=environment_variables,
        )

    def kill_container(self, container_name: str):
        try:
            container = self._client.containers.get(container_name)
        except NotFound:
            logger.info(f"Not found container of name {container_name}")
            return

        if _check_container_in_network(container, self._network):
            logger.info(f"Disconnecting container {container.name} from network...")
            self._network.disconnect(container)

        logger.info("Stopping container...")
        container.stop()
        logger.info("Removing container...")
        container.remove(force=True)

    def _wait_for_preparation_is_done(self):
        # Try 2 times to check if preparation is done. If not, raise exception.
        retry_times = 2
        while not _check_if_preparation_is_done(self._client):
            retry_times -= 1
            if retry_times == 0:
                raise Exception("Preparation work for executor container is not done.")

            logger.warning("Preparation work for executor container is not done yet. Wait for 5 seconds.")
            time.sleep(5)


executor_image_manager = ExecutorImageManager.get_instance()


def _check_if_preparation_is_done(client: docker.DockerClient) -> bool:
    # Check if network exists.
    client = docker.DockerClient(base_url=DOCKER_SOCKET_PATH)
    network_name = _get_network_name()
    network_list = client.networks.list(names=[network_name])
    if len(network_list) == 0:
        logger.warning(f"Network {network_name} has not been created.")
        return False

    # Check if runtime container is in network.
    network = network_list[0]
    runtime_container = client.containers.get(os.environ.get("HOSTNAME"))
    if not _check_container_in_network(runtime_container, network):
        logger.warning(f"Runtime container is not added into network {network_name}.")
        return False

    # Check if executor image is pulled.
    for lang, image in language_to_default_image.items():
        if len(client.images.list(name=image)) == 0:
            logger.warning(f"Image {image} for language {lang} has not been pulled.")
            return False

    return True


def prepare_for_executor_containers():
    client = docker.DockerClient(base_url=DOCKER_SOCKET_PATH)

    # Creating network if not created before.
    network_name = _get_network_name()
    network_list = client.networks.list(names=[network_name])
    if len(network_list) > 0:
        logger.info(f"Network {network_name} already exists.")
        network = network_list[0]
    else:
        logger.info(f"Creating network {network_name}...")
        network = client.networks.create(network_name, driver="bridge")

    # Add runtime container to network.
    runtime_container = client.containers.get(os.environ.get("HOSTNAME"))
    if _check_container_in_network(runtime_container, network):
        logger.info(f"Container {runtime_container.name} is already in network {network.name}.")
    else:
        logger.info(f"Adding container {runtime_container.name} in network {network.name}...")
        network.connect(runtime_container)

    # Pull image if not existed.
    for lang, image in language_to_default_image.items():
        if len(client.images.list(name=image)) == 0:
            logger.info(f"Pulling image {image} for language {lang}")
            client.images.pull(image)
            logger.info(f"Succeed to pull image {image} for language {lang}")


def finalize_for_executor_containers():
    """Disconnect all containers from network and remove network."""
    client = docker.DockerClient(base_url=DOCKER_SOCKET_PATH)
    network_name = _get_network_name()
    network_list = client.networks.list(names=[network_name])
    if len(network_list) > 0:
        network: Network = network_list[0]
        containers = client.containers.list(all=True)
        # Disconnect all containers from network and kill containers which are not runtime container.
        for container in containers:
            if not _check_container_in_network(container, network):
                continue
            try:
                network.disconnect(container)
                # Do not stop runtime container.
                if container.name == os.environ.get("HOSTNAME"):
                    continue
                logger.info("Stopping container...")
                container.stop()
                logger.info("Removing container...")
                container.remove(force=True)
            except Exception as ex:
                logger.warning(f"Failed to stop or remove container {container.name}. Exception: {ex}")

        logger.info(f"Removing network {network_name}...")
        network.remove()
