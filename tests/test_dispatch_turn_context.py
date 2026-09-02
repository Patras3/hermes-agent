"""Regression tests for request correlation reaching plugin tool handlers."""

import importlib
import json

import model_tools
from hermes_cli.plugins import PluginContext, PluginManager, PluginManifest
from tools.registry import ToolRegistry


_TOOL_NAME = "test_plugin_turn_context"
_TOOL_SCHEMA = {
    "name": _TOOL_NAME,
    "description": "Capture immutable turn context for dispatch tests.",
    "parameters": {"type": "object", "properties": {}},
}


def _register_plugin_tool(monkeypatch, handler) -> None:
    registry_module = importlib.import_module("tools.registry")
    registry = ToolRegistry()
    monkeypatch.setattr(registry_module, "registry", registry)
    monkeypatch.setattr(model_tools, "registry", registry)

    manager = PluginManager()
    context = PluginContext(PluginManifest(name="turn-context-test"), manager)
    context.register_tool(
        name=_TOOL_NAME,
        toolset="plugin_turn_context_test",
        schema=_TOOL_SCHEMA,
        handler=handler,
    )


def _dispatch(function_name=_TOOL_NAME, function_args=None, **context):
    return json.loads(
        model_tools.handle_function_call(
            function_name,
            function_args or {},
            skip_pre_tool_call_hook=True,
            skip_tool_request_middleware=True,
            **context,
        )
    )


def _assert_turn_context(
    captured, *, task_id, session_id, turn_id, tool_call_id, api_request_id
):
    context_keys = (
        "task_id",
        "session_id",
        "turn_id",
        "tool_call_id",
        "api_request_id",
    )
    assert {key: captured.get(key) for key in context_keys} == {
        "task_id": task_id,
        "session_id": session_id,
        "turn_id": turn_id,
        "tool_call_id": tool_call_id,
        "api_request_id": api_request_id,
    }
    assert captured.get("user_task") is None


def test_plugin_handler_receives_full_turn_context_without_user_task(monkeypatch):
    captured = {}

    def handler(_args, **kwargs):
        captured.update(kwargs)
        return json.dumps({"accepted": True})

    _register_plugin_tool(monkeypatch, handler)

    result = _dispatch(
        task_id="task-1",
        session_id="session-1",
        turn_id="turn-1",
        tool_call_id="tool-call-1",
        api_request_id="api-request-1",
    )

    assert result == {"accepted": True}
    _assert_turn_context(
        captured,
        task_id="task-1",
        session_id="session-1",
        turn_id="turn-1",
        tool_call_id="tool-call-1",
        api_request_id="api-request-1",
    )


def test_plugin_handler_receives_turn_context_through_tool_call_bridge(monkeypatch):
    captured = {}

    def handler(_args, **kwargs):
        captured.update(kwargs)
        return json.dumps({"accepted": True})

    _register_plugin_tool(monkeypatch, handler)

    result = _dispatch(
        function_name="tool_call",
        function_args={"name": _TOOL_NAME, "arguments": {}},
        task_id="task-bridge",
        session_id="session-bridge",
        turn_id="turn-bridge",
        tool_call_id="tool-call-bridge",
        api_request_id="api-request-bridge",
        enabled_toolsets=["plugin_turn_context_test"],
    )

    assert result == {"accepted": True}
    _assert_turn_context(
        captured,
        task_id="task-bridge",
        session_id="session-bridge",
        turn_id="turn-bridge",
        tool_call_id="tool-call-bridge",
        api_request_id="api-request-bridge",
    )


def test_plugin_handler_preserves_stale_and_cross_turn_boundaries(monkeypatch):
    trusted_turns = {
        "session-a": "turn-a",
        "session-b": "turn-b",
    }

    def handler(_args, **kwargs):
        session_id = kwargs.get("session_id")
        turn_id = kwargs.get("turn_id")
        expected_turn = (
            trusted_turns.get(session_id) if isinstance(session_id, str) else None
        )
        if expected_turn != turn_id:
            return json.dumps({"error": "untrusted turn context"})
        return json.dumps({"accepted": True})

    _register_plugin_tool(monkeypatch, handler)

    assert _dispatch(
        session_id="session-a",
        turn_id="turn-a",
        tool_call_id="tool-call-a",
        api_request_id="api-request-a",
    ) == {"accepted": True}
    assert _dispatch(
        session_id="session-a",
        turn_id="stale-turn",
        tool_call_id="tool-call-stale",
        api_request_id="api-request-stale",
    ) == {"error": "untrusted turn context"}
    assert _dispatch(
        session_id="session-b",
        turn_id="turn-a",
        tool_call_id="tool-call-cross-session",
        api_request_id="api-request-cross-session",
    ) == {"error": "untrusted turn context"}
    assert _dispatch(
        session_id="session-b",
        turn_id="turn-b",
        tool_call_id="tool-call-b",
        api_request_id="api-request-b",
    ) == {"accepted": True}
