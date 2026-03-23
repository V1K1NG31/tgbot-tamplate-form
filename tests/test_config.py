"""Tests for ``src.core.config.Settings``."""

import importlib

import pytest


def test_settings_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.setenv("ADMIN_CHAT_ID", "-100")
    monkeypatch.setenv("ADMIN_IDS", "[1, 2]")
    monkeypatch.setenv("REDIS_URL", "redis://example:6379/1")

    import src.core.config as cfg

    importlib.reload(cfg)

    assert cfg.settings.bot_token == "test-token"
    assert cfg.settings.admin_chat_id == -100
    assert cfg.settings.admin_ids == [1, 2]
    assert cfg.settings.redis_url == "redis://example:6379/1"
