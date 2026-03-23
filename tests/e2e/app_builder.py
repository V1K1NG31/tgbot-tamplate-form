"""Build Bot + Dispatcher matching ``app/main.py`` (MemoryStorage + fake API)."""

from __future__ import annotations

from dataclasses import dataclass

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from fluentogram import TranslatorHub

from src.core.config import settings
from src.core.fluent import create_translator_hub, set_default_hub
from src.handlers import setup_routers
from src.handlers.user.form_scene import FormScene
from src.middlewares import setup_middlewares
from tests.e2e.fake_telegram_session import FakeTelegramSession


@dataclass(frozen=True)
class E2EApp:
    """Wired application for ``feed_update`` tests."""

    bot: Bot
    dp: Dispatcher
    hub: TranslatorHub
    session: FakeTelegramSession


def build_e2e_app() -> E2EApp:
    """
    Mirror ``app/main.py`` wiring: hub, middleware, routers, ``FormScene``.

    Differs only in storage (memory) and Bot session (``FakeTelegramSession``).
    """
    hub = create_translator_hub()
    set_default_hub(hub)
    session = FakeTelegramSession()
    bot = Bot(
        token=settings.bot_token,
        session=session,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher(
        storage=MemoryStorage(),
        events_isolation=SimpleEventIsolation(),
    )
    setup_middlewares(dp)
    setup_routers(dp)
    registry = SceneRegistry(dp)
    registry.add(FormScene)
    return E2EApp(bot=bot, dp=dp, hub=hub, session=session)
