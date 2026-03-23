"""Shared pytest fixtures."""

import os

# Required before importing any module that loads ``src.core.config``.
os.environ.setdefault("BOT_TOKEN", "pytest-dummy-token")
os.environ.setdefault("ADMIN_CHAT_ID", "-1")

import pytest
from fluentogram import TranslatorHub, TranslatorRunner

from src.core.fluent import create_translator_hub


@pytest.fixture
def translator_hub() -> TranslatorHub:
    """Fluent translator hub backed by ``locales/en.ftl``."""
    return create_translator_hub()


@pytest.fixture
def i18n(translator_hub: TranslatorHub) -> TranslatorRunner:
    """English ``TranslatorRunner`` for keyboard tests."""
    return translator_hub.get_translator_by_locale("en")
