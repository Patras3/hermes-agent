"""Tests for system-prompt model-identity sync across provider failover.

The system prompt is session-stable and embeds ``Model:``/``Provider:``
identity lines.  When ``try_activate_fallback`` swaps the runtime, the
prompt must be rewritten in place (and synced into the in-flight
``api_messages``) or the agent reports the primary model's name while a
fallback model is answering — e.g. a local gemma fallback claiming to be
gpt-5.4-mini after a Codex usage-limit 429.
"""

from types import SimpleNamespace

from agent.chat_completion_helpers import rewrite_prompt_model_identity
from agent.conversation_loop import _sync_failover_system_message


_PROMPT = (
    "You are a helpful assistant.\n"
    "\n"
    "Memory note at line start:\n"
    "Model: decoy-from-memory\n"
    "\n"
    "Conversation started: Wednesday, June 10, 2026\n"
    "Model: gpt-5.4-mini\n"
    "Provider: openai-codex"
)


def _agent(prompt=_PROMPT, ephemeral=None, model="gpt-5.4-mini", provider="openai-codex"):
    return SimpleNamespace(
        _cached_system_prompt=prompt,
        ephemeral_system_prompt=ephemeral,
        model=model,
        provider=provider,
        pass_session_id=False,
        session_id="sess-failover",
        _session_metadata_line="",
    )


class TestRewritePromptModelIdentity:
    def test_swaps_identity_lines_to_fallback_runtime(self):
        agent = _agent()
        rewrite_prompt_model_identity(agent, "gemma4:e2b-mlx", "custom")
        assert "Model: gemma4:e2b-mlx" in agent._cached_system_prompt
        assert "Provider: custom" in agent._cached_system_prompt
        assert "Model: gpt-5.4-mini" not in agent._cached_system_prompt
        assert "Provider: openai-codex" not in agent._cached_system_prompt

    def test_only_last_occurrence_is_rewritten(self):
        agent = _agent()
        rewrite_prompt_model_identity(agent, "gemma4:e2b-mlx", "custom")
        # Earlier matching lines may be user content (memory snapshots,
        # context files) and must survive untouched.
        assert "Model: decoy-from-memory" in agent._cached_system_prompt

    def test_round_trip_restores_byte_identical_prompt(self):
        # restore_primary_runtime rewrites the lines back; the result must
        # match the stored prompt byte-for-byte so the primary's prefix
        # cache still hits after restoration.
        agent = _agent()
        rewrite_prompt_model_identity(agent, "gemma4:e2b-mlx", "custom")
        rewrite_prompt_model_identity(agent, "gpt-5.4-mini", "openai-codex")
        assert agent._cached_system_prompt == _PROMPT

    def test_noop_when_prompt_missing_or_empty(self):
        for prompt in (None, ""):
            agent = _agent(prompt=prompt)
            rewrite_prompt_model_identity(agent, "m", "p")
            assert agent._cached_system_prompt == prompt

    def test_empty_values_leave_lines_unchanged(self):
        agent = _agent()
        rewrite_prompt_model_identity(agent, "", "")
        assert agent._cached_system_prompt == _PROMPT


class TestSyncFailoverSystemMessage:
    def test_patches_in_flight_system_message(self):
        agent = _agent()
        rewrite_prompt_model_identity(agent, "gemma4:e2b-mlx", "custom")
        api_messages = [
            {"role": "system", "content": _PROMPT},
            {"role": "user", "content": "what model are you?"},
        ]
        result = _sync_failover_system_message(agent, api_messages, _PROMPT)
        assert "Model: gemma4:e2b-mlx" in api_messages[0]["content"]
        assert result == agent._cached_system_prompt

    def test_keeps_ephemeral_out_of_in_flight_system_message(self):
        agent = _agent(ephemeral="Stay terse.")
        api_messages = [{"role": "system", "content": _PROMPT}]
        _sync_failover_system_message(agent, api_messages, _PROMPT)
        assert api_messages[0]["content"] == agent._cached_system_prompt
        assert "Stay terse." not in api_messages[0]["content"]

    def test_updates_current_user_metadata_sidecar(self):
        agent = _agent(model="fallback-model", provider="fallback-provider")
        old_sidecar = (
            "what model?\n\n"
            "[Conversation started: Wednesday, June 10, 2026\n"
            "Model: primary-model\n"
            "Provider: primary-provider]\n\n"
            "PLUGIN-CTX"
        )
        conversation_messages = [
            {"role": "user", "content": "what model?", "api_content": old_sidecar}
        ]
        api_messages = [
            {"role": "system", "content": _PROMPT},
            {"role": "user", "content": old_sidecar},
        ]

        _sync_failover_system_message(
            agent,
            api_messages,
            _PROMPT,
            conversation_messages,
            0,
        )

        updated = conversation_messages[0]["api_content"]
        assert "Model: fallback-model" in updated
        assert "Provider: fallback-provider" in updated
        assert "Model: primary-model" not in updated
        assert updated.endswith("\n\nPLUGIN-CTX")
        assert api_messages[1]["content"] == updated

    def test_noop_without_cached_prompt(self):
        agent = _agent(prompt=None)
        api_messages = [{"role": "system", "content": "original"}]
        result = _sync_failover_system_message(agent, api_messages, "active")
        assert api_messages[0]["content"] == "original"
        assert result == "active"

    def test_noop_when_first_message_is_not_system(self):
        agent = _agent()
        api_messages = [{"role": "user", "content": "hi"}]
        result = _sync_failover_system_message(agent, api_messages, "active")
        assert api_messages == [{"role": "user", "content": "hi"}]
        # Still returns the cached prompt for subsequent call-block rebuilds.
        assert result == agent._cached_system_prompt
