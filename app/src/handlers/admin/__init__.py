"""Admin handlers (placeholder router)."""

from aiogram import Dispatcher, Router


def register_admin_handlers(dp: Dispatcher) -> None:
    """Register admin handlers (empty until you add commands)."""
    router = Router()
    dp.include_router(router)
