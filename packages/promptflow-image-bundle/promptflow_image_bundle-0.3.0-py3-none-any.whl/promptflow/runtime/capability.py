""" define runtime capability, which describes the features and apis supported by current runtime. """
from dataclasses import dataclass

from promptflow._internal import Feature, FeatureState, get_feature_list

RUNTIME = "runtime"  # runtime component name
EXECUTOR = "executor"  # executor component name


@dataclass
class Api:
    """The dataclass to describe an api."""

    verb: str
    route: list
    version: str
    description: str

    def to_dict(self):
        return {"verb": self.verb, "route": self.route, "version": self.version, "description": self.description}


def get_runtime_api_list():
    # define current runtime api list.
    runtime_api_list = [
        Api(
            verb="GET",
            route=["/package_tools", "/aml-api/v1.0/package_tools"],
            version="1.0",
            description="Get tools supported by runtime.",
        ),
        Api(
            verb="POST",
            route=["/submit_single_node", "/aml-api/v1.0/submit_single_node"],
            version="1.0",
            description="Submit single node to runtime.",
        ),
        Api(
            verb="POST",
            route=["/submit_flow", "/aml-api/v1.0/submit_flow"],
            version="1.0",
            description="Submit flow to runtime.",
        ),
        Api(
            verb="POST",
            route=["/submit_bulk_run", "/aml-api/v1.0/submit_bulk_run"],
            version="1.0",
            description="Submit bulk run to runtime.",
        ),
        Api(
            verb="POST",
            route=["/meta-v2", "/aml-api/v1.0/meta-v2/"],
            version="1.0",
            description="Generate tool meta-v2.",
        ),
        Api(
            verb="GET",
            route=["/health", "/aml-api/v1.0/health"],
            version="1.0",
            description="Check if the runtime is alive.",
        ),
        Api(
            verb="GET",
            route=["/version", "/aml-api/v1.0/version"],
            version="1.0",
            description="Check the runtime's version.",
        ),
        Api(
            verb="POST",
            route=["/dynamic_list", "/aml-api/v1.0/dynamic_list"],
            version="1.0",
            description="Dynamically generates a list of items for a tool input.",
        ),
        Api(
            verb="POST",
            route=["/retrieve_tool_func_result", "/aml-api/v1.0/retrieve_tool_func_result"],
            version="1.0",
            description="Retrieve generated result of a tool function.",
        ),
        Api(
            verb="POST",
            route=["/submit_flow_async", "/aml-api/v1.0/submit_flow_async"],
            version="1.0",
            description="Submit async flow test to runtime.",
        ),
        Api(
            verb="POST",
            route=["/submit_single_node_async", "/aml-api/v1.0/submit_single_node_async"],
            version="1.0",
            description="Submit async single node to runtime.",
        ),
        Api(
            verb="POST",
            route=["/cancel_run", "/aml-api/v1.0/cancel_run"],
            version="1.0",
            description="Cancel async flow test or single node run.",
        ),
    ]

    runtime_api_list = [runtime_api.to_dict() for runtime_api in runtime_api_list]
    return runtime_api_list


def get_runtime_with_executor_feature_list():
    # define feature list that need both runtime and executor sign off.
    runtime_with_executor_feature_list = [
        Feature(
            name="CSharpFlowBatchRun",
            description="c# flow batch run support",
            state=FeatureState.READY,
        ),
    ]
    return runtime_with_executor_feature_list


def get_runtime_only_feature_list():
    # define feature list that only need runtime sign off.
    runtime_only_feature_list = [
        Feature(
            name="AsyncFlow",
            description="Async flow test and single node run support",
            state=FeatureState.READY,
        ),
    ]
    return runtime_only_feature_list


def get_executor_feature_list():
    executor_feature_list = get_feature_list()
    return executor_feature_list


def get_merged_feature_list(runtime_with_executor_feature_list, runtime_only_feature_list, executor_feature_list):
    """merge runtime feature list and executor feature list."""
    runtime_with_executor_feature_dict = {
        runtime_with_executor_feature.name: runtime_with_executor_feature
        for runtime_with_executor_feature in runtime_with_executor_feature_list
    }
    merged_feature_list = []

    for executor_feature in executor_feature_list:
        executor_feature_name = executor_feature.name
        if executor_feature_name in runtime_with_executor_feature_dict.keys():
            # for feature in both runtime and executor, merge them
            runtime_with_executor_feature = runtime_with_executor_feature_dict[executor_feature_name]
            merged_feature_state_value = get_merged_feature_state_value(
                runtime_with_executor_feature.state, executor_feature.state
            )
            merged_feature = get_merged_feature(
                runtime_with_executor_feature.name,
                runtime_with_executor_feature.description,
                {
                    RUNTIME: merged_feature_state_value,
                    EXECUTOR: merged_feature_state_value,
                },
            )
            merged_feature_list.append(merged_feature)
            runtime_with_executor_feature_dict.pop(executor_feature_name, None)
        else:
            # for feature that only need executor sign off, copy executor state to runtime component
            merged_feature = get_merged_feature(
                executor_feature.name,
                executor_feature.description,
                {RUNTIME: executor_feature.state.value, EXECUTOR: executor_feature.state.value},
            )
            merged_feature_list.append(merged_feature)

    # for feature that only need runtime sign off, copy runtime state to executor component
    runtime_only_feature_list = [
        get_merged_feature(
            runtime_only_feature.name,
            runtime_only_feature.description,
            {RUNTIME: runtime_only_feature.state.value, EXECUTOR: runtime_only_feature.state.value},
        )
        for runtime_only_feature in runtime_only_feature_list
    ]
    merged_feature_list = merged_feature_list + runtime_only_feature_list

    return merged_feature_list


def get_total_feature_list():
    """get all current feature list that should be returned to pfs."""
    return get_merged_feature_list(
        get_runtime_with_executor_feature_list(), get_runtime_only_feature_list(), get_executor_feature_list()
    )


def get_merged_feature(name, description, state):
    return {"name": name, "description": description, "state": state}


def get_merged_feature_state_value(runtime_state: FeatureState, executor_state: FeatureState):
    if runtime_state == FeatureState.E2ETEST or executor_state == FeatureState.E2ETEST:
        return FeatureState.E2ETEST.value
    return FeatureState.READY.value
