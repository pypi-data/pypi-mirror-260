from pathlib import Path
from typing import Any, Union

from promptflow.contracts.run_info import FlowRunInfo, RunInfo
from promptflow.runtime.data import prepare_data
from promptflow.runtime.utils import logger
from promptflow.runtime.utils.downloader import _get_last_part_of_uri


def convert_url_to_path(flow_file: Path, original_data: Any, base_dir: Path):
    """
    Convert universal link to path for multimedia data before pass to executor.
    For example: {"data:image/jpg;url": "azureml://example/logo.jpg"} -> {"data:image/jpg;path": "logo.jpg"}

    :param flow_file: The path to the YAML file. The YAML content will be used to determine the contract version.
    :type flow_file: Path
    :param original_data: Original data that need to be converted, such as flow inputs and dependency node outputs.
    :type original_data: Any
    :param base_dir: The base dir to download the multimedia data.
    :type base_dir: Path
    :return: The content with multimedia format that is changed to path.
    :rtype: Any
    """
    try:
        from promptflow._utils.multimedia_data_converter import (
            AbstractMultimediaInfoConverter,
            MultimediaConverter,
            MultimediaInfo,
            ResourceType,
        )
    except Exception:
        logger.warning("Please upgrade promptflow package to 1.4.1 or higher version for async image support.")
        return original_data

    class UrlToPathConverter(AbstractMultimediaInfoConverter):
        def __init__(self, base_dir: Path):
            self._base_dir = base_dir

        def convert(self, info: MultimediaInfo) -> MultimediaInfo:
            if info.resource_type != ResourceType.URL:
                return info
            if not info.content.startswith("azureml:"):
                return info
            prepare_data(info.content, self._base_dir)
            file_name = _get_last_part_of_uri(info.content)
            file_path = (self._base_dir / file_name).as_posix()
            new_info = MultimediaInfo(
                mime_type=info.mime_type,
                resource_type=ResourceType.PATH,
                content=file_path,
            )
            return new_info

    multimedia_converter = MultimediaConverter(flow_file)
    url_to_path_converter = UrlToPathConverter(base_dir)
    return multimedia_converter.convert_content_recursively(original_data, url_to_path_converter)


def convert_path_to_url(flow_file: Path, original_data: Any, base_universal_link: str):
    """
    Convert path to universal link for multimedia data before persist to blob storage.
    For example: {"data:image/jpg;path": "logo.jpg"} -> {"data:image/jpg;url": "azureml://example.com/logo.jpg"}

    :param flow_file: The path to the YAML file. The YAML content will be used to determine the contract version.
    :type flow_file: Path
    :param original_data: Original data that need to be converted, such as node outputs.
    :type original_data: Any
    :param base_universal_link: The base universal link that multimedia data should be uploaded to.
    :type base_universal_link: str
    :return: The content with multimedia format that is changed to universal link.
    :rtype: Any
    """
    try:
        from promptflow._utils.multimedia_data_converter import (
            AbstractMultimediaInfoConverter,
            MultimediaConverter,
            MultimediaInfo,
            ResourceType,
        )
    except Exception:
        logger.warning("Please upgrade promptflow package to 1.4.1 or higher version for async image support.")
        return original_data

    class PathToUrlConverter(AbstractMultimediaInfoConverter):
        def __init__(self, base_universal_link: str):
            self._base_universal_link = base_universal_link

        def convert(self, info: MultimediaInfo) -> MultimediaInfo:
            if info.resource_type != ResourceType.PATH:
                return info
            path = Path(info.content)
            if path.is_absolute():
                logger.error(
                    "Image path should be relative path, {customer_content} can't be converted to universal link.",
                    extra={"customer_content": info.content},
                )
                return info

            # to trim starting "./" in "./a/b.jpg"
            file_path = path.relative_to(".").as_posix()
            universal_link = f"{self._base_universal_link}/{file_path}"
            new_info = MultimediaInfo(
                mime_type=info.mime_type,
                resource_type=ResourceType.URL,
                content=universal_link,
            )
            return new_info

    multimedia_converter = MultimediaConverter(flow_file)
    path_to_url_converter = PathToUrlConverter(base_universal_link)
    return multimedia_converter.convert_content_recursively(original_data, path_to_url_converter)


def convert_path_to_url_for_run_info(flow_file: Path, run_info: Union[FlowRunInfo, RunInfo], base_universal_link: str):
    """
    Convert path to universal link for multimedia data before persist node run infos or flow run infos to blob storage.
    This function apply convert_path_to_url function to inputs, output and api_calls fields in FlowRunInfo or RunInfo,
    and replace original value with the returned value in FlowRunInfo or RunInfo.

    :param flow_file: The path to the YAML file. The YAML content will be used to determine the contract version.
    :type flow_file: Path
    :param run_info: Flow run info or node run info that need to be converted.
    :type run_info: Union[FlowRunInfo, RunInfo]
    :param base_universal_link: The base universal link that multimedia data should be uploaded to.
    :type base_universal_link: str
    """
    if run_info.inputs:
        run_info.inputs = convert_path_to_url(flow_file, run_info.inputs, base_universal_link)
    if run_info.output:
        output_data = convert_path_to_url(flow_file, run_info.output, base_universal_link)
        run_info.output = output_data
    if run_info.api_calls:
        run_info.api_calls = convert_path_to_url(flow_file, run_info.api_calls, base_universal_link)
