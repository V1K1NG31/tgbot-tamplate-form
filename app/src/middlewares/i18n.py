"""Injects TranslatorRunner as ``i18n`` into handler data."""

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from fluentogram import TranslatorHub


class TranslatorMiddleware(BaseMiddleware):
    """Injects TranslatorRunner as ``i18n`` into handler data."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        hub: TranslatorHub = data["translator_hub"]
        data["i18n"] = hub.get_translator_by_locale("en")
        return await handler(event, data)
