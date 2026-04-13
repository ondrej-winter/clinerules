#!/usr/bin/env python3
"""Log selected PreToolUse tool arguments and always allow them.

Tool argument logging is explicit and tool-specific. Extend the formatter
mapping below as additional tools need structured summaries.
"""

from __future__ import annotations

from collections.abc import Callable
import json
from datetime import datetime
from pathlib import Path
import sys


ToolArgumentFormatter = Callable[[dict[str, object]], str]


def _stringify_one_line(value: object) -> str:
    try:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    except TypeError:
        text = str(value)
    return ' '.join(text.splitlines())


def _format_value(value: object) -> str:
    if value is None:
        return 'N/A'
    return _stringify_one_line(value)


def _format_path(parameters: dict[str, object]) -> str:
    return _format_value(parameters.get('path') or parameters.get('absolutePath'))


def _format_key_values(parameters: dict[str, object], *keys: str) -> str:
    parts = [f"{key}={_format_value(parameters.get(key))}" for key in keys]
    return ', '.join(parts) if parts else 'no arguments'


def _format_search_files(parameters: dict[str, object]) -> str:
    return _format_key_values(parameters, 'path', 'regex', 'file_pattern')


def _format_access_mcp_resource(parameters: dict[str, object]) -> str:
    return _format_key_values(parameters, 'server_name', 'uri')


def _format_ask_followup_question(parameters: dict[str, object]) -> str:
    return _format_key_values(parameters, 'question')


def _format_attempt_completion(parameters: dict[str, object]) -> str:
    return _format_key_values(parameters, 'result', 'command')


def _format_browser_action(parameters: dict[str, object]) -> str:
    return _format_key_values(parameters, 'action', 'url', 'coordinate', 'text')


def _format_execute_command(parameters: dict[str, object]) -> str:
    return _format_key_values(parameters, 'command', 'requires_approval')


def _format_new_task(parameters: dict[str, object]) -> str:
    return _format_key_values(parameters, 'context')


def _format_plan_mode_respond(parameters: dict[str, object]) -> str:
    return _format_key_values(parameters, 'response')


def _format_use_mcp_tool(parameters: dict[str, object]) -> str:
    return _format_key_values(parameters, 'server_name', 'tool_name')


def _format_web_fetch(parameters: dict[str, object]) -> str:
    return _format_key_values(parameters, 'url', 'prompt')


def _format_no_arguments(_: dict[str, object]) -> str:
    return 'no arguments'


SUPPORTED_TOOL_ARGUMENT_FORMATTERS: dict[str, ToolArgumentFormatter] = {
    'write_to_file': _format_path,
    'read_file': _format_path,
    'replace_in_file': _format_path,
    'search_files': _format_search_files,
    'list_files': _format_path,
    'list_code_definition_names': _format_path,
    'access_mcp_resource': _format_access_mcp_resource,
    'ask_followup_question': _format_ask_followup_question,
    'attempt_completion': _format_attempt_completion,
    'browser_action': _format_browser_action,
    'execute_command': _format_execute_command,
    'focus_chain': _format_no_arguments,
    'load_mcp_documentation': _format_no_arguments,
    'new_task': _format_new_task,
    'plan_mode_respond': _format_plan_mode_respond,
    'use_mcp_tool': _format_use_mcp_tool,
    'web_fetch': _format_web_fetch,
}


def get_tracked_tool_arguments(tool_name: str, parameters: dict[str, object]) -> str:
    """Return a structured argument summary for a supported tool."""

    formatter = SUPPORTED_TOOL_ARGUMENT_FORMATTERS.get(tool_name)
    if formatter:
        try:
            return formatter(parameters)
        except Exception as error:
            return (
                f'format_error={_stringify_one_line(error)}, '
                f'raw_parameters={_stringify_one_line(parameters)}'
            )

    return f'unsupported tool, raw_parameters={_stringify_one_line(parameters)}'


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({'cancel': False}))
        return 0

    workspace_roots = payload.get('workspaceRoots') or []
    workspace_root = workspace_roots[0] if workspace_roots else None

    try:
        pre_tool_use = payload.get('preToolUse') or {}
        tool_name = pre_tool_use.get('toolName') or pre_tool_use.get('tool') or 'unknown'
        parameters = pre_tool_use.get('parameters') or {}
        tool_arguments = get_tracked_tool_arguments(tool_name, parameters)
    except Exception as error:
        tool_name = 'unknown'
        tool_arguments = (
            f'payload_error={_stringify_one_line(error)}, '
            f'raw_payload={_stringify_one_line(payload)}'
        )

    if workspace_root:
        log_dir = Path(workspace_root) / '.cline-logs'
        log_file = log_dir / 'cline-file-activity.log'

        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            with log_file.open('a', encoding='utf-8') as handle:
                handle.write(
                    f"{datetime.now().strftime('%H:%M:%S')} - {tool_name}: {tool_arguments}\n"
                )
        except OSError:
            pass

    print(json.dumps({'cancel': False}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
