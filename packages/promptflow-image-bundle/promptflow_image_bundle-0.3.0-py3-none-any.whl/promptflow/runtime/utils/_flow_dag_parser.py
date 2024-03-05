from ruamel.yaml import YAML

from promptflow.runtime._errors import FlowFileNotFound, InvalidFlowYaml

DEFAULT_LANGUAGE = "python"


def get_language(dag_file_path) -> str:
    try:
        yaml = YAML()
        with open(dag_file_path, "r") as f:
            flow_dag = yaml.load(f)
            return flow_dag.get("language", DEFAULT_LANGUAGE)
    except FileNotFoundError as ex:
        raise FlowFileNotFound(f"Cannot find flow file. Error message={str(ex)}") from ex
    except Exception as ex:
        raise InvalidFlowYaml(message=f"Failed to read dag yaml file. Error message={str(ex)}") from ex
