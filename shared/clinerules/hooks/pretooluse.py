#!/usr/bin/env python3
"""Log supported PreToolUse tool arguments and always allow them.

Current support is explicit and tool-specific. `read_file` logs its file path,
and the mapping below is ready to extend with more tools as needed.
"""

from __future__ import annotations

from collections.abc import Callable
import json
from datetime import datetime
from pathlib import Path
import sys


ToolArgumentFormatter = Callable[[dict[str, object]], str]


def _format_value(value: object) -> str:
    if value is None:
        return 'N/A'
    return str(value)


def _format_path(parameters: dict[str, object]) -> str:
    return _format_value(parameters.get('path') or parameters.get('absolutePath'))


def _format_key_values(parameters: dict[str, object], *keys: str) -> str:
    parts = [f"{key}={_format_value(parameters.get(key))}" for key in keys]
    return ', '.join(parts) if parts else 'no arguments'


SUPPORTED_TOOL_ARGUMENT_FORMATTERS: dict[str, ToolArgumentFormatter] = {
    # File and directory tools.
    'write_to_file': _format_path,
    'read_file': _format_path,
    'replace_in_file': _format_path,
    'search_files': _format_key_values,
    'list_files': _format_path,
    'list_code_definition_names': _format_path,
    # General tools requested for support.
    'access_mcp_resource': lambda parameters: _format_key_values(parameters, 'server_name', 'uri'),
    'ask_followup_question': lambda parameters: _format_key_values(parameters, 'question'),
    'attempt_completion': lambda parameters: _format_key_values(parameters, 'result', 'command'),
    'browser_action': lambda parameters: _format_key_values(parameters, 'action', 'url', 'coordinate', 'text'),
    'execute_command': lambda parameters: _format_key_values(parameters, 'command'),
    'focus_chain': lambda parameters: 'no arguments',
    'load_mcp_documentation': lambda parameters: 'no arguments',
    'new_task': lambda parameters: _format_key_values(parameters, 'context'),
    'plan_mode_respond': lambda parameters: _format_key_values(parameters, 'response'),
    'use_mcp_tool': lambda parameters: _format_key_values(parameters, 'server_name', 'tool_name'),
    'web_fetch': lambda parameters: _format_key_values(parameters, 'url', 'prompt'),
}


def get_tracked_tool_arguments(tool_name: str, parameters: dict[str, object]) -> str:
    """Return the tracked argument summary for a supported tool.

    Today we explicitly support `read_file` plus several other tool shapes.
    Add new tool formatters to `SUPPORTED_TOOL_ARGUMENT_FORMATTERS` as more
    tools need structured logging.
    """

    formatter = SUPPORTED_TOOL_ARGUMENT_FORMATTERS.get(tool_name)
    if formatter:
        if tool_name == 'search_files':
            return _format_key_values(parameters, 'path', 'regex', 'file_pattern')
        return formatter(parameters)

    return 'unsupported tool'


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({'cancel': False}))
        return 0

    workspace_roots = payload.get('workspaceRoots') or []
    workspace_root = workspace_roots[0] if workspace_roots else None

    pre_tool_use = payload.get('preToolUse') or {}
    tool_name = pre_tool_use.get('toolName') or pre_tool_use.get('tool') or 'unknown'
    parameters = pre_tool_use.get('parameters') or {}
    tool_arguments = get_tracked_tool_arguments(tool_name, parameters)

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
