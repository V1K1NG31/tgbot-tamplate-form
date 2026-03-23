"""Tests for i18n middleware registration."""

from unittest.mock import MagicMock

import pytest

from src.middlewares import setup_middlewares
from src.middlewares.i18n import TranslatorMiddleware


@pytest.mark.asyncio
async def test_translator_middleware_injects_i18n(translator_hub) -> None:
    """Handler data receives English ``TranslatorRunner`` as ``i18n``."""
    mw = TranslatorMiddleware()
    seen_i18n = None

    async def handler(_event, data):
        nonlocal seen_i18n
        seen_i18n = data.get("i18n")
        return "done"

    data: dict = {"translator_hub": translator_hub}
    result = await mw(handler, MagicMock(), data)
    assert result == "done"
    assert seen_i18n is not None
    assert seen_i18n.start.message() == translator_hub.get_translator_by_locale(
        "en"
    ).start.message()


def test_setup_middlewares_registers_on_message_and_callback() -> None:
    """Outer middleware is attached for messages and callback queries."""
    dp = MagicMock()
    setup_middlewares(dp)
    dp.message.outer_middleware.register.assert_called_once()
    dp.callback_query.outer_middleware.register.assert_called_once()
