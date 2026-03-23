"""Middleware registration."""

from aiogram import Dispatcher

from src.middlewares.i18n import TranslatorMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    """Register middleware on the dispatcher."""
    middleware = TranslatorMiddleware()
    dp.message.outer_middleware.register(middleware)
    dp.callback_query.outer_middleware.register(middleware)
