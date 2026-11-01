"""Typing loops may remove only their own channel registry entry."""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from gateway.config import PlatformConfig
from plugins.platforms.discord.adapter import DiscordAdapter


@pytest.mark.asyncio
async def test_stopping_old_typing_loop_preserves_restart(monkeypatch, tmp_path):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    adapter = DiscordAdapter(PlatformConfig(enabled=True, token="test-token"))
    started = asyncio.Queue()
    old_cancelled = asyncio.Event()
    finish_old = asyncio.Event()
    replacement_cancelled = asyncio.Event()
    old_task = None
    tasks = []

    async def request(_route):
        task = asyncio.current_task()
        started.put_nowait(task)
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            if task is old_task:
                old_cancelled.set()
                # Hold the old loop before its finally while a replacement starts.
                await finish_old.wait()
            else:
                replacement_cancelled.set()
            raise

    adapter._client = SimpleNamespace(http=SimpleNamespace(request=request))
    chat_id = "12345"
    try:
        await adapter.send_typing(chat_id)
        old_task = adapter._typing_tasks[chat_id]
        tasks.append(old_task)
        assert await started.get() is old_task

        stopping = asyncio.create_task(adapter.stop_typing(chat_id))
        tasks.append(stopping)
        await old_cancelled.wait()
        await adapter.send_typing(chat_id)
        replacement = adapter._typing_tasks[chat_id]
        tasks.append(replacement)
        assert await started.get() is replacement

        finish_old.set()
        await stopping
        assert adapter._typing_tasks.get(chat_id) is replacement
        assert not replacement.done()

        await adapter.send_typing(chat_id)
        assert adapter._typing_tasks[chat_id] is replacement
        await adapter.stop_typing(chat_id)
        assert replacement_cancelled.is_set()
        assert replacement.done()
        assert chat_id not in adapter._typing_tasks
    finally:
        finish_old.set()
        # Also clean up the orphan on the unfixed implementation (RED).
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


@pytest.mark.asyncio
async def test_failed_typing_loop_releases_own_entry_for_restart(monkeypatch, tmp_path):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    adapter = DiscordAdapter(PlatformConfig(enabled=True, token="test-token"))
    request = AsyncMock(side_effect=RuntimeError("transport failed"))
    adapter._client = SimpleNamespace(http=SimpleNamespace(request=request))
    chat_id = "12345"

    await adapter.send_typing(chat_id)
    first = adapter._typing_tasks[chat_id]
    await first
    assert chat_id not in adapter._typing_tasks

    await adapter.send_typing(chat_id)
    replacement = adapter._typing_tasks[chat_id]
    await replacement
    assert replacement is not first
    assert chat_id not in adapter._typing_tasks
    assert request.await_count == 2
