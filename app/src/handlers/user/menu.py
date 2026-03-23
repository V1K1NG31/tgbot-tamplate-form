"""Menu callback handlers."""

from typing import cast

from aiogram.fsm.scene import ScenesManager
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner

from src.handlers.user.form_scene import FormScene
from src.keyboards.menu import (
    build_detail_keyboard,
    build_menu_keyboard,
)
from src.utils.telegram import editable_message_from_callback

SECTIONS: dict[str, tuple[str, bool]] = {
    "menu_what": ("menu-what", True),
    "menu_duration": ("menu-duration", True),
    "menu_price": ("menu-price", True),
    "menu_travel": ("menu-travel", True),
    "menu_property": ("menu-property", True),
    "menu_debts": ("menu-debts", True),
    "menu_remote": ("menu-remote", True),
    "menu_docs": ("menu-docs", True),
}


async def handle_menu_section(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
) -> None:
    """Show a section: edit message when detail keyboard is used."""
    data = callback.data
    if data is None:
        await callback.answer()
        return
    ftl_key, with_detail = SECTIONS[cast(str, data)]
    text = i18n.get(ftl_key)

    if with_detail:
        keyboard = build_detail_keyboard(
            contact_label=i18n.btn.contact.lawyer(),
            back_label=i18n.btn.back(),
        )
        msg = editable_message_from_callback(callback)
        if msg is None:
            await callback.answer()
            return
        await msg.edit_text(text, reply_markup=keyboard)
    else:
        raw = callback.message
        if raw is None:
            await callback.answer()
            return
        chat = raw.chat
        if chat is None:
            await callback.answer()
            return
        bot = callback.bot
        if bot is None:
            await callback.answer()
            return
        await bot.send_message(
            chat_id=chat.id,
            text=text,
        )
    await callback.answer()


async def handle_menu_back(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
) -> None:
    """Return to the main menu (edit current message)."""
    msg = editable_message_from_callback(callback)
    if msg is None:
        await callback.answer()
        return
    await msg.edit_text(
        i18n.start.message(),
        reply_markup=build_menu_keyboard().as_markup(),
    )
    await callback.answer()


async def handle_enter_form(
    _callback: CallbackQuery,
    scenes: ScenesManager,
) -> None:
    """Enter the form scene (menu_form / menu_contact)."""
    await scenes.enter(FormScene)
