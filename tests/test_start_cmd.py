"""/start handler tests."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.handlers.user.start import cmd_start


@pytest.mark.asyncio
async def test_cmd_start_sends_welcome_and_menu(i18n) -> None:
    """Welcome text and reply markup are passed to ``answer``."""
    message = MagicMock()
    message.answer = AsyncMock()
    await cmd_start(message, i18n)
    message.answer.assert_awaited_once()
    args, kwargs = message.answer.call_args
    assert args[0] == i18n.start.message()
    assert kwargs.get("reply_markup") is not None
