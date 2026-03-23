"""Tests for menu handler wiring (static maps)."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.handlers.user import menu
from src.handlers.user.form_scene import FormScene
from src.handlers.user.menu import (
    SECTIONS,
    handle_enter_form,
    handle_menu_back,
    handle_menu_section,
)


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


@pytest.mark.asyncio
async def test_handle_menu_section_answers_when_data_none(i18n) -> None:
    callback = MagicMock()
    callback.data = None
    callback.answer = AsyncMock()
    await handle_menu_section(callback, i18n)
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_handle_menu_section_answers_when_not_editable(i18n) -> None:
    callback = MagicMock()
    callback.data = "menu_what"
    callback.answer = AsyncMock()
    with patch.object(
        menu,
        "editable_message_from_callback",
        return_value=None,
    ):
        await handle_menu_section(callback, i18n)
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_handle_menu_section_edits_when_detail_keyboard(i18n) -> None:
    callback = MagicMock()
    callback.data = "menu_what"
    callback.answer = AsyncMock()
    msg = MagicMock()
    msg.edit_text = AsyncMock()
    with patch.object(
        menu,
        "editable_message_from_callback",
        return_value=msg,
    ):
        await handle_menu_section(callback, i18n)
    msg.edit_text.assert_awaited_once()
    assert msg.edit_text.call_args[0][0] == i18n.get("menu-what")
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_handle_menu_section_plain_branch_missing_message(i18n) -> None:
    extra_key = "menu_test_no_detail"
    with patch.dict(
        menu.SECTIONS,
        {extra_key: ("menu-what", False)},
        clear=False,
    ):
        callback = MagicMock()
        callback.data = extra_key
        callback.message = None
        callback.answer = AsyncMock()
        await handle_menu_section(callback, i18n)
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_handle_menu_section_plain_branch_missing_chat(i18n) -> None:
    extra_key = "menu_test_no_detail"
    with patch.dict(
        menu.SECTIONS,
        {extra_key: ("menu-what", False)},
        clear=False,
    ):
        callback = MagicMock()
        callback.data = extra_key
        callback.message = MagicMock()
        callback.message.chat = None
        callback.answer = AsyncMock()
        await handle_menu_section(callback, i18n)
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_handle_menu_section_plain_branch_missing_bot(i18n) -> None:
    extra_key = "menu_test_no_detail"
    with patch.dict(
        menu.SECTIONS,
        {extra_key: ("menu-what", False)},
        clear=False,
    ):
        callback = MagicMock()
        callback.data = extra_key
        callback.message = MagicMock()
        callback.message.chat = MagicMock()
        callback.message.chat.id = 1
        callback.bot = None
        callback.answer = AsyncMock()
        await handle_menu_section(callback, i18n)
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_handle_menu_section_send_message_without_detail(i18n) -> None:
    """Branch when ``with_detail`` is false uses ``bot.send_message``."""
    extra_key = "menu_test_no_detail"
    with patch.dict(
        menu.SECTIONS,
        {extra_key: ("menu-what", False)},
        clear=False,
    ):
        callback = MagicMock()
        callback.data = extra_key
        callback.message = MagicMock()
        callback.message.chat = MagicMock()
        callback.message.chat.id = 42
        callback.bot = MagicMock()
        callback.bot.send_message = AsyncMock()
        callback.answer = AsyncMock()
        await handle_menu_section(callback, i18n)
    callback.bot.send_message.assert_awaited_once_with(
        chat_id=42,
        text=i18n.get("menu-what"),
    )
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_handle_menu_back_answers_when_not_editable(i18n) -> None:
    callback = MagicMock()
    callback.answer = AsyncMock()
    with patch.object(
        menu,
        "editable_message_from_callback",
        return_value=None,
    ):
        await handle_menu_back(callback, i18n)
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_handle_menu_back_edits_to_main_menu(i18n) -> None:
    callback = MagicMock()
    callback.answer = AsyncMock()
    msg = MagicMock()
    msg.edit_text = AsyncMock()
    with patch.object(
        menu,
        "editable_message_from_callback",
        return_value=msg,
    ):
        await handle_menu_back(callback, i18n)
    msg.edit_text.assert_awaited_once()
    assert msg.edit_text.call_args[0][0] == i18n.start.message()
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_handle_enter_form_enters_form_scene() -> None:
    scenes = MagicMock()
    scenes.enter = AsyncMock()
    callback = MagicMock()
    await handle_enter_form(callback, scenes)
    scenes.enter.assert_awaited_once_with(FormScene)
