"""Offline Telegram Bot API session for E2E tests (no HTTP)."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from typing import Any

from aiogram.client.bot import Bot
from aiogram.client.session.base import BaseSession
from aiogram.methods import AnswerCallbackQuery, EditMessageText, SendMessage
from aiogram.methods.base import TelegramMethod, TelegramType
from aiogram.types import Message


class FakeTelegramSession(BaseSession):
    """
    Records API calls and returns valid in-memory ``Message`` / ``bool``.

    Used with ``Dispatcher.feed_update`` so handlers run real ``Bot`` methods
    without contacting api.telegram.org.
    """

    def __init__(self) -> None:
        super().__init__()
        self.calls: list[dict[str, Any]] = []
        self._message_id_seq = 0

    def _next_message_id(self) -> int:
        self._message_id_seq += 1
        return self._message_id_seq

    async def close(self) -> None:
        """No underlying HTTP client."""

    async def stream_content(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:
        if False:
            yield b""

    def _record_call(self, method: TelegramMethod[TelegramType]) -> None:
        name = type(method).__name__
        entry: dict[str, Any] = {"api": name}
        if isinstance(method, SendMessage):
            entry["chat_id"] = method.chat_id
            entry["text"] = method.text
        elif isinstance(method, EditMessageText):
            entry["chat_id"] = method.chat_id
            entry["message_id"] = method.message_id
            entry["text"] = method.text
        elif isinstance(method, AnswerCallbackQuery):
            entry["callback_query_id"] = method.callback_query_id
        self.calls.append(entry)

    async def make_request(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: int | None = None,
    ) -> TelegramType:
        self._record_call(method)

        if isinstance(method, AnswerCallbackQuery):
            return True  # type: ignore[return-value]

        if isinstance(method, EditMessageText):
            if method.message_id is None:
                msg = "FakeTelegramSession: inline EditMessageText not supported"
                raise NotImplementedError(msg)
            msg_id = method.message_id
        elif isinstance(method, SendMessage):
            msg_id = self._next_message_id()
        else:
            msg = (
                f"FakeTelegramSession: unsupported method {type(method).__name__}. "
                "Add a branch or extend the fake."
            )
            raise NotImplementedError(msg)

        chat_id = method.chat_id
        text = method.text or ""
        payload = {
            "message_id": msg_id,
            "date": int(datetime.now(UTC).timestamp()),
            "chat": {"id": chat_id, "type": "private"},
            "text": text,
        }
        return Message.model_validate(payload, context={"bot": bot})
