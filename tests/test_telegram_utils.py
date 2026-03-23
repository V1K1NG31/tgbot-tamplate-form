"""Tests for ``src.utils.telegram``."""

from datetime import UTC, datetime
from unittest.mock import MagicMock

from aiogram.types import Chat, InaccessibleMessage, Message

from src.utils.telegram import editable_message_from_callback


def test_editable_message_returns_none_when_message_missing() -> None:
    callback = MagicMock()
    callback.message = None
    assert editable_message_from_callback(callback) is None


def test_editable_message_returns_none_for_inaccessible() -> None:
    chat = Chat(id=1, type="private")
    inacc = InaccessibleMessage(chat=chat, message_id=42)
    callback = MagicMock()
    callback.message = inacc
    assert editable_message_from_callback(callback) is None


def test_editable_message_returns_regular_message() -> None:
    chat = Chat(id=1, type="private")
    msg = Message(
        message_id=7,
        date=datetime.now(UTC),
        chat=chat,
    )
    callback = MagicMock()
    callback.message = msg
    assert editable_message_from_callback(callback) is msg
