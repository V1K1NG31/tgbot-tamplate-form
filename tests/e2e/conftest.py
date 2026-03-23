"""E2E fixtures: full dispatcher + fake Telegram session."""

from collections.abc import AsyncIterator

import pytest

import src.core.fluent as fluent
from tests.e2e.app_builder import E2EApp, build_e2e_app


@pytest.fixture
async def e2e_app() -> AsyncIterator[E2EApp]:
    """
    Bot and dispatcher wired like ``app/main.py`` (memory storage, fake API).

    Restores the previous default Fluent hub after the test.
    """
    previous_hub = fluent._hub_slot[0]
    app = build_e2e_app()
    try:
        yield app
    finally:
        fluent._hub_slot[0] = previous_hub
        await app.bot.session.close()
