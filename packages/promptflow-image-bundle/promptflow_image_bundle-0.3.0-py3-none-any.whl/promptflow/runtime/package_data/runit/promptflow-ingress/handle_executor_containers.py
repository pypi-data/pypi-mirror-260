# TODO: Refactor into a prt module. Python file in runit folder is not conventional.


import argparse
import enum

from promptflow.runtime.executor_image_manager import finalize_for_executor_containers, prepare_for_executor_containers


class Stage(enum.Enum):
    INIT = "init"
    FINALIZE = "finalize"


def _handle_executor_containers(stage):
    # TODO: Remove try/catch
    # This is a guarding logic to make sure runtime container is started up successfully
    # even when this script fails.
    if stage == Stage.INIT:
        try:
            prepare_for_executor_containers()
        except Exception as ex:
            print(f"Failed to prepare executor containers. Exception: {ex}")
    elif stage == Stage.FINALIZE:
        try:
            finalize_for_executor_containers()
        except Exception as ex:
            print(f"Failed to finalize executor containers. Exception: {ex}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Handle executor containers.")
    parser.add_argument("--stage", type=Stage, choices=list(Stage), help="Stage can be either 'init' or 'finalize'")
    args = parser.parse_args()
    _handle_executor_containers(args.stage)
