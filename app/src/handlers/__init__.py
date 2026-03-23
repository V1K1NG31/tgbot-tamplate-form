"""Router registration."""

from aiogram import Dispatcher

from src.handlers.admin import register_admin_handlers
from src.handlers.user import register_user_handlers


def setup_routers(dp: Dispatcher) -> None:
    """Register all routers on the dispatcher."""
    register_user_handlers(dp)
    register_admin_handlers(dp)
