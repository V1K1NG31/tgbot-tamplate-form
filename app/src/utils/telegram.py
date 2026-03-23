"""Helpers for Telegram / aiogram types."""

from aiogram.types import CallbackQuery, InaccessibleMessage, Message


def editable_message_from_callback(callback: CallbackQuery) -> Message | None:
    """
    Callback message suitable for edit_* (not None, not InaccessibleMessage).
    """
    msg = callback.message
    if msg is None:
        return None
    if isinstance(msg, InaccessibleMessage):
        return None
    return msg
