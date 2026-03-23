"""Tests for ``src.core.fluent``."""

import pytest

import src.core.fluent as fluent


def test_create_translator_hub_english_start_message() -> None:
    hub = fluent.create_translator_hub()
    i18n = hub.get_translator_by_locale("en")
    text = i18n.start.message()
    assert "demo" in text.lower()
    assert "Svetlitsa" in text


def test_get_default_i18n_requires_hub() -> None:
    previous = fluent._hub_slot[0]
    fluent._hub_slot[0] = None
    try:
        with pytest.raises(RuntimeError, match="translator hub not set"):
            fluent.get_default_i18n()
    finally:
        fluent._hub_slot[0] = previous


def test_set_default_hub_and_get_default_i18n() -> None:
    previous = fluent._hub_slot[0]
    hub = fluent.create_translator_hub()
    fluent.set_default_hub(hub)
    try:
        i18n = fluent.get_default_i18n()
        assert "individual" in i18n.form.q0().lower()
    finally:
        fluent._hub_slot[0] = previous
