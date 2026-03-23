"""Tests for menu handler wiring (static maps)."""

from src.handlers.user.menu import SECTIONS


def test_menu_sections_cover_all_menu_callbacks() -> None:
    assert "menu_what" in SECTIONS
    assert "menu_duration" in SECTIONS
    assert "menu_price" in SECTIONS
    assert "menu_travel" in SECTIONS
    assert "menu_property" in SECTIONS
    assert "menu_debts" in SECTIONS
    assert "menu_remote" in SECTIONS
    assert "menu_docs" in SECTIONS


def test_menu_sections_use_ftl_keys_with_detail_flag() -> None:
    ftl_key, with_detail = SECTIONS["menu_what"]
    assert ftl_key == "menu-what"
    assert with_detail is True
