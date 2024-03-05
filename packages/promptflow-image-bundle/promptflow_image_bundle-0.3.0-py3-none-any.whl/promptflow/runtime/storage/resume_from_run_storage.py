import json
from pathlib import Path
from typing import Dict, List

from promptflow._utils.multimedia_utils import load_multimedia_data_recursively, resolve_multimedia_data_recursively
from promptflow.contracts.run_info import FlowRunInfo
from promptflow.contracts.run_info import RunInfo as NodeRunInfo
from promptflow.storage._run_storage import AbstractBatchRunStorage


class ResumeFromRunStorage(AbstractBatchRunStorage):
    LINE_NUMBER_WIDTH = 9

    def __init__(
        self,
        resume_from_run_debug_info_dir: Path,
    ) -> None:
        self._resume_from_run_flow_artifact_folder = resume_from_run_debug_info_dir / "flow_artifacts"
        self._resume_from_run_node_artifact_folder = resume_from_run_debug_info_dir / "node_artifacts"
        self._loaded_flow_run_info_dict = {}  # {line_number: flow_run_info}

        # load flow run info in dict
        self._load_all_flow_run_info()

    def load_node_run_info_for_line(self, line_number: int) -> List[NodeRunInfo]:
        node_run_infos = []
        for node_folder in sorted(self._resume_from_run_node_artifact_folder.iterdir()):
            filename = f"{str(line_number).zfill(self.LINE_NUMBER_WIDTH)}.jsonl"
            node_run_record_file = node_folder / filename
            if node_run_record_file.is_file():
                runs = self._load_info_from_file(node_run_record_file)
                run = resolve_multimedia_data_recursively(node_run_record_file, runs[0])
                run = load_multimedia_data_recursively(run)
                run_info = NodeRunInfo.deserialize(run)
                node_run_infos.append(run_info)
        if len(node_run_infos) == 0:
            return None
        return node_run_infos

    def load_flow_run_info(self, line_number: int) -> FlowRunInfo:
        run = self._loaded_flow_run_info_dict.get(line_number)
        if run is None:
            return None
        run = load_multimedia_data_recursively(run)
        run_info = FlowRunInfo.deserialize(run)
        return run_info

    def _load_info_from_file(self, file_path):
        run_infos = []
        if file_path.suffix.lower() == ".jsonl":
            with open(file_path) as f:
                run_infos = [json.loads(line)["run_info"] for line in list(f)]
        return run_infos

    def _load_all_flow_run_info(self) -> List[Dict]:
        for line_run_record_file in sorted(self._resume_from_run_flow_artifact_folder.iterdir()):
            new_runs = self._load_info_from_file(line_run_record_file)
            for new_run in new_runs:
                new_run = resolve_multimedia_data_recursively(line_run_record_file, new_run)
                line_number = new_run.get("index")
                self._loaded_flow_run_info_dict[line_number] = new_run
