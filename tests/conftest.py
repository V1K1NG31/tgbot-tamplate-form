"""Shared pytest fixtures."""

from __future__ import annotations

import pytest
from fluentogram import TranslatorHub, TranslatorRunner

import tests._bootstrap_env  # noqa: F401  # side effect: load .env.test*
from src.core.fluent import create_translator_hub


def pytest_configure(config: pytest.Config) -> None:
    """Reserved for future pytest-wide hooks."""
    _ = config


@pytest.fixture
def translator_hub() -> TranslatorHub:
    """Fluent translator hub backed by ``locales/en.ftl``."""
    return create_translator_hub()


@pytest.fixture
def i18n(translator_hub: TranslatorHub) -> TranslatorRunner:
    """English ``TranslatorRunner`` for keyboard tests."""
    return translator_hub.get_translator_by_locale("en")
