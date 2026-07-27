"""Regression tests for optional SSH sync and session persistence."""

from unittest.mock import MagicMock

from tools.environments import ssh as ssh_env
import tools.terminal_tool as terminal_tool


def _stub_ssh_init(monkeypatch):
    monkeypatch.setattr(ssh_env.shutil, "which", lambda _name: "/usr/bin/ssh")
    monkeypatch.setattr(ssh_env.SSHEnvironment, "_establish_connection", lambda self: None)
    monkeypatch.setattr(ssh_env.SSHEnvironment, "_detect_remote_home", lambda self: "/root")
    monkeypatch.setattr(ssh_env.SSHEnvironment, "_ensure_remote_dirs", lambda self: None)


def test_ssh_file_sync_can_be_disabled(monkeypatch):
    _stub_ssh_init(monkeypatch)
    sync_factory = MagicMock()
    init_session = MagicMock()
    monkeypatch.setattr(ssh_env, "FileSyncManager", sync_factory)
    monkeypatch.setattr(ssh_env.SSHEnvironment, "init_session", init_session)

    env = ssh_env.SSHEnvironment(
        host="example.com",
        user="root",
        file_sync_enabled=False,
    )

    sync_factory.assert_not_called()
    assert env._sync_manager is None


def test_ssh_persistent_shell_can_be_disabled(monkeypatch):
    _stub_ssh_init(monkeypatch)
    init_session = MagicMock()
    monkeypatch.setattr(ssh_env.SSHEnvironment, "init_session", init_session)

    ssh_env.SSHEnvironment(
        host="example.com",
        user="root",
        file_sync_enabled=False,
        persistent_shell=False,
    )

    init_session.assert_not_called()


def test_ssh_factory_forwards_sync_and_persistence_flags(monkeypatch):
    captured = {}
    sentinel = object()

    def fake_ssh_environment(**kwargs):
        captured.update(kwargs)
        return sentinel

    monkeypatch.setattr(terminal_tool, "_SSHEnvironment", fake_ssh_environment)

    env = terminal_tool._create_environment(
        env_type="ssh",
        image="unused",
        cwd="/root",
        timeout=30,
        ssh_config={
            "host": "example.com",
            "user": "root",
            "port": 22,
            "key": "/tmp/test-key",
            "persistent": False,
            "file_sync_enabled": False,
        },
    )

    assert env is sentinel
    assert captured["persistent_shell"] is False
    assert captured["file_sync_enabled"] is False


def test_terminal_config_reads_ssh_file_sync_flag(monkeypatch):
    monkeypatch.setenv("TERMINAL_ENV", "ssh")
    monkeypatch.setenv("TERMINAL_SSH_HOST", "example.com")
    monkeypatch.setenv("TERMINAL_SSH_USER", "root")
    monkeypatch.setenv("TERMINAL_FILE_SYNC_ENABLED", "false")

    config = terminal_tool._get_env_config()

    assert config["file_sync_enabled"] is False
