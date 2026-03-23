"""Bot entrypoint."""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.fsm.storage.redis import RedisStorage

from src.core.config import settings
from src.core.fluent import create_translator_hub, set_default_hub
from src.handlers import setup_routers
from src.handlers.user.form_scene import FormScene
from src.middlewares import setup_middlewares


async def main() -> None:
    """Run the bot (polling)."""
    hub = create_translator_hub()
    set_default_hub(hub)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    storage = RedisStorage.from_url(
        settings.redis_url,
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    dp = Dispatcher(
        storage=storage,
        events_isolation=SimpleEventIsolation(),
    )
    setup_middlewares(dp)
    setup_routers(dp)

    scene_registry = SceneRegistry(dp)
    scene_registry.add(FormScene)

    try:
        await dp.start_polling(bot, translator_hub=hub)
    finally:
        await storage.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
