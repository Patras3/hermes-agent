"""Regression tests for request correlation reaching plugin tool handlers."""

import importlib
import json

import model_tools
import pytest
from hermes_cli.plugins import PluginContext, PluginManager, PluginManifest
from tools.registry import ToolRegistry


_TOOL_NAME = "test_plugin_turn_context"
_TOOL_SCHEMA = {
    "name": _TOOL_NAME,
    "description": "Capture immutable turn context for dispatch tests.",
    "parameters": {"type": "object", "properties": {}},
}
_DISPATCH_CONTEXT = {
    "task_id": "task-1",
    "session_id": "session-1",
    "turn_id": "turn-1",
    "tool_call_id": "tool-call-1",
    "api_request_id": "api-request-1",
    "user_task": "user-task-1",
}


def _register_plugin_tool(monkeypatch, handler, *, is_async=False) -> None:
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
        is_async=is_async,
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


def _dispatch_path(via_bridge, **context):
    if via_bridge:
        return _dispatch(
            function_name="tool_call",
            function_args={"name": _TOOL_NAME, "arguments": {}},
            enabled_toolsets=["plugin_turn_context_test"],
            **context,
        )
    return _dispatch(**context)


def _assert_turn_context(
    captured,
    *,
    task_id,
    session_id,
    turn_id,
    tool_call_id,
    api_request_id,
    user_task,
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
    assert captured.get("user_task") == user_task


@pytest.mark.parametrize("via_bridge", [False, True], ids=["direct", "bridge"])
@pytest.mark.parametrize("is_async", [False, True], ids=["sync", "async"])
def test_legacy_plugin_handler_ignores_new_turn_context(
    monkeypatch, via_bridge, is_async
):
    captured = {}

    if is_async:

        async def async_handler(_args, task_id, session_id, user_task):
            captured.update(
                task_id=task_id,
                session_id=session_id,
                user_task=user_task,
            )
            return json.dumps({"accepted": True})

        handler = async_handler
    else:

        def sync_handler(_args, task_id, session_id, user_task):
            captured.update(
                task_id=task_id,
                session_id=session_id,
                user_task=user_task,
            )
            return json.dumps({"accepted": True})

        handler = sync_handler

    _register_plugin_tool(monkeypatch, handler, is_async=is_async)

    result = _dispatch_path(via_bridge, **_DISPATCH_CONTEXT)

    assert result == {"accepted": True}
    assert captured == {
        "task_id": "task-1",
        "session_id": "session-1",
        "user_task": "user-task-1",
    }


@pytest.mark.parametrize("via_bridge", [False, True], ids=["direct", "bridge"])
@pytest.mark.parametrize("is_async", [False, True], ids=["sync", "async"])
def test_explicit_plugin_handler_receives_exact_turn_context(
    monkeypatch, via_bridge, is_async
):
    captured = {}

    if is_async:

        async def async_handler(
            _args,
            task_id,
            session_id,
            user_task,
            turn_id,
            tool_call_id,
            api_request_id,
        ):
            captured.update(
                task_id=task_id,
                session_id=session_id,
                user_task=user_task,
                turn_id=turn_id,
                tool_call_id=tool_call_id,
                api_request_id=api_request_id,
            )
            return json.dumps({"accepted": True})

        handler = async_handler
    else:

        def sync_handler(
            _args,
            task_id,
            session_id,
            user_task,
            turn_id,
            tool_call_id,
            api_request_id,
        ):
            captured.update(
                task_id=task_id,
                session_id=session_id,
                user_task=user_task,
                turn_id=turn_id,
                tool_call_id=tool_call_id,
                api_request_id=api_request_id,
            )
            return json.dumps({"accepted": True})

        handler = sync_handler

    _register_plugin_tool(monkeypatch, handler, is_async=is_async)

    result = _dispatch_path(via_bridge, **_DISPATCH_CONTEXT)

    assert result == {"accepted": True}
    _assert_turn_context(captured, **_DISPATCH_CONTEXT)


@pytest.mark.parametrize("via_bridge", [False, True], ids=["direct", "bridge"])
@pytest.mark.parametrize("is_async", [False, True], ids=["sync", "async"])
def test_kwargs_plugin_handler_receives_exact_turn_context(
    monkeypatch, via_bridge, is_async
):
    captured = {}

    if is_async:

        async def async_handler(_args, **kwargs):
            captured.update(kwargs)
            return json.dumps({"accepted": True})

        handler = async_handler
    else:

        def sync_handler(_args, **kwargs):
            captured.update(kwargs)
            return json.dumps({"accepted": True})

        handler = sync_handler

    _register_plugin_tool(monkeypatch, handler, is_async=is_async)

    result = _dispatch_path(via_bridge, **_DISPATCH_CONTEXT)

    assert result == {"accepted": True}
    assert captured == _DISPATCH_CONTEXT


@pytest.mark.parametrize("via_bridge", [False, True], ids=["direct", "bridge"])
@pytest.mark.parametrize("is_async", [False, True], ids=["sync", "async"])
def test_plugin_handler_internal_type_error_is_not_retried_or_masked(
    monkeypatch, via_bridge, is_async
):
    calls = 0

    if is_async:

        async def async_handler(_args, **_kwargs):
            nonlocal calls
            calls += 1
            raise TypeError("handler-body-sentinel")

        handler = async_handler
    else:

        def sync_handler(_args, **_kwargs):
            nonlocal calls
            calls += 1
            raise TypeError("handler-body-sentinel")

        handler = sync_handler

    _register_plugin_tool(monkeypatch, handler, is_async=is_async)

    result = _dispatch_path(via_bridge, **_DISPATCH_CONTEXT)

    assert calls == 1
    assert "TypeError: handler-body-sentinel" in result["error"]


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
