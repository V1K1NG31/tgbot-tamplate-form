from aiogram import Dispatcher, F, Router
from aiogram.filters import CommandStart

from src.handlers.user.menu import (
    SECTIONS,
    handle_enter_form,
    handle_menu_back,
    handle_menu_section,
)
from src.handlers.user.start import cmd_start


def register_user_handlers(dp: Dispatcher) -> None:
    """Register user-facing handlers."""
    router = Router()

    router.message.register(cmd_start, CommandStart())

    router.callback_query.register(
        handle_menu_back,
        F.data == "menu_back",
    )
    router.callback_query.register(
        handle_enter_form,
        F.data == "menu_form",
    )
    router.callback_query.register(
        handle_enter_form,
        F.data == "menu_contact",
    )
    router.callback_query.register(
        handle_menu_section,
        F.data.in_(SECTIONS),
    )

    dp.include_router(router)
