from dataclasses import dataclass
from typing import List

from promptflow.runtime.utils._contract_util import normalize_dict_keys_camel_to_snake


@dataclass
class LogFilteringPolicy:
    """Settings for Log Filtering Policy"""

    filtering_patterns: List[str]

    @staticmethod
    def deserialize(data: dict) -> "LogFilteringPolicy":
        data = normalize_dict_keys_camel_to_snake(data)

        log_filtering_policy = LogFilteringPolicy(
            filtering_patterns=data.get("filtering_patterns", []),
        )

        return log_filtering_policy


@dataclass
class PredefinedPolicies:
    """Settings for Predefined Policies"""

    log_filtering_policy: LogFilteringPolicy = None

    @staticmethod
    def deserialize(data: dict) -> "PredefinedPolicies":
        data = normalize_dict_keys_camel_to_snake(data)

        predefined_policies = PredefinedPolicies(
            log_filtering_policy=LogFilteringPolicy.deserialize(data.get("log_filtering_policy", {})),
        )

        return predefined_policies
