"""/start command handler."""

from aiogram.types import Message
from fluentogram import TranslatorRunner

from src.keyboards.menu import build_menu_keyboard


async def cmd_start(message: Message, i18n: TranslatorRunner) -> None:
    """Reply with the welcome text and main menu."""
    await message.answer(
        i18n.start.message(),
        reply_markup=build_menu_keyboard().as_markup(),
    )
