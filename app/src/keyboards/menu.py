from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_menu_keyboard() -> InlineKeyboardBuilder:
    """Main inline menu (two columns, sorted by label length)."""
    builder = InlineKeyboardBuilder()
    buttons = [
        ("What is Svetlitsa?", "menu_what"),
        ("Timeline (demo)", "menu_duration"),
        ("Pricing (demo)", "menu_price"),
        ("How we meet", "menu_travel"),
        ("Deliverables", "menu_property"),
        ("What we cover", "menu_debts"),
        ("Remote-first", "menu_remote"),
        ("Brief & assets", "menu_docs"),
        ("Fill out the form", "menu_form"),
    ]
    buttons.sort(key=lambda item: len(item[0]))
    for text, data in buttons:
        builder.add(InlineKeyboardButton(text=text, callback_data=data))
    builder.adjust(2)
    return builder


def build_detail_keyboard(
    contact_label: str,
    back_label: str,
) -> InlineKeyboardMarkup:
    """Keyboard: open form + back."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=contact_label,
            callback_data="menu_contact",
        ),
    )
    builder.add(
        InlineKeyboardButton(
            text=back_label,
            callback_data="menu_back",
        ),
    )
    builder.adjust(1)
    return builder.as_markup()
