# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import re

import promptflow
from promptflow import runtime
from promptflow.exceptions import ErrorTarget

# TODO: Support stacktrace log for built-in-tools
_tools_support_error_stacktrace_logging = []


def get_promptflow_code_paths():
    promptflow_root_path = os.path.dirname(os.path.abspath(promptflow.__file__))
    runtime_root_path = os.path.dirname(os.path.dirname(os.path.abspath(runtime.__file__)))

    # When running locally, part of the code comes from src/promptflow folder,
    # and another part of the code come from the legacy src/promptflow-sdk folder.
    #
    # When they are installed as pip packages, they share the same folder (site-packages/promptflow).
    #
    # For most of the cases, they have the same value. Use `set` to remove the duplicated values.
    promptflow_code_paths = set([promptflow_root_path, runtime_root_path])
    return promptflow_code_paths


def need_filter_external_stacktrace(reference_code):
    if not reference_code:
        return True
    if (
        reference_code.startswith(ErrorTarget.TOOL.value)
        and reference_code not in _tools_support_error_stacktrace_logging
    ):
        return True
    return False


def filter_external_stacktrace(stacktrace):
    if not stacktrace:
        return ""

    promptflow_code_paths = get_promptflow_code_paths()
    code_paths_sub_pattern = "|".join([re.escape(path) for path in promptflow_code_paths])
    pattern = re.compile(r'File "(?!' + code_paths_sub_pattern + ")[^\n]*, line [^\n]*, in [^\n]*\n")
    match = pattern.search(stacktrace)
    if match is not None:
        return stacktrace[: match.start()] + "[REDACTED: External StackTrace]\n"
    return stacktrace


def _extract_stacktrace(debug_info: dict, filter_external: bool):
    if debug_info is not None and len(debug_info) > 0:
        yield from _extract_stacktrace(debug_info.get("innerException", {}), filter_external)

        stack_trace = debug_info.get("stackTrace", "")
        if filter_external:
            stack_trace = filter_external_stacktrace(stack_trace)
        yield stack_trace


def generate_safe_error_stacktrace(error_response: dict):
    error = error_response.get("error", {})
    debug_info = error.get("debugInfo", {})

    reference_code = error.get("referenceCode", "")
    filter_external = need_filter_external_stacktrace(reference_code)

    return "".join(_extract_stacktrace(debug_info, filter_external))
