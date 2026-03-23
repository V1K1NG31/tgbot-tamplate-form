"""Tests for inline keyboards."""

from fluentogram import TranslatorRunner

from src.keyboards.form import (
    build_form_step0_keyboard,
    build_form_step1_keyboard,
)
from src.keyboards.menu import build_menu_keyboard


def _all_callback_data(markup: object) -> set[str]:
    rows = markup.inline_keyboard
    out: set[str] = set()
    for row in rows:
        for btn in row:
            if btn.callback_data is not None:
                out.add(btn.callback_data)
    return out


def test_menu_keyboard_includes_all_section_callbacks() -> None:
    kb = build_menu_keyboard().as_markup()
    data = _all_callback_data(kb)
    assert "menu_what" in data
    assert "menu_form" in data
    assert "menu_docs" in data


def test_form_step0_keyboard_person_and_back(i18n: TranslatorRunner) -> None:
    kb = build_form_step0_keyboard(i18n)
    data = _all_callback_data(kb)
    assert "form_individual" in data
    assert "form_sole_proprietor" in data
    assert "form_back" in data


def test_form_step1_keyboard_debt_options(i18n: TranslatorRunner) -> None:
    kb = build_form_step1_keyboard(i18n)
    data = _all_callback_data(kb)
    assert "form_debt_up300" in data
    assert "form_debt_exact" in data
