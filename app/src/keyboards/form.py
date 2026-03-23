"""Inline keyboards for the form scene."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

PERSON_TYPE_OPTIONS = [
    ("form-individual", "form_individual"),
    ("form-sole-proprietor", "form_sole_proprietor"),
]

DEBT_OPTIONS = [
    ("form-debt-up300", "form_debt_up300"),
    ("form-debt-300-500", "form_debt_300_500"),
    ("form-debt-500-1m", "form_debt_500_1m"),
    ("form-debt-1m-plus", "form_debt_1m_plus"),
    ("form-debt-exact", "form_debt_exact"),
]

ARREARS_OPTIONS = [
    ("form-arrears-1m", "form_arrears_1m"),
    ("form-arrears-6m", "form_arrears_6m"),
    ("form-arrears-1y", "form_arrears_1y"),
    ("form-arrears-ontime", "form_arrears_ontime"),
]


def build_form_step0_keyboard(
    i18n: TranslatorRunner,
) -> InlineKeyboardMarkup:
    """Step 1: individual or company."""
    builder = InlineKeyboardBuilder()
    for ftl_key, cb_data in PERSON_TYPE_OPTIONS:
        builder.add(
            InlineKeyboardButton(
                text=i18n.get(ftl_key),
                callback_data=cb_data,
            )
        )
    builder.add(
        InlineKeyboardButton(
            text=i18n.btn.back(),
            callback_data="form_back",
        )
    )
    builder.adjust(2)
    return builder.as_markup()


def build_form_step1_keyboard(
    i18n: TranslatorRunner,
) -> InlineKeyboardMarkup:
    """Step 2: scope tier."""
    builder = InlineKeyboardBuilder()
    for ftl_key, cb_data in DEBT_OPTIONS:
        builder.add(
            InlineKeyboardButton(
                text=i18n.get(ftl_key),
                callback_data=cb_data,
            )
        )
    builder.add(
        InlineKeyboardButton(
            text=i18n.btn.back(),
            callback_data="form_back",
        )
    )
    builder.adjust(2)
    return builder.as_markup()


def build_form_step2_keyboard(
    i18n: TranslatorRunner,
) -> InlineKeyboardMarkup:
    """Step 3: desired start timeline."""
    builder = InlineKeyboardBuilder()
    for ftl_key, cb_data in ARREARS_OPTIONS:
        builder.add(
            InlineKeyboardButton(
                text=i18n.get(ftl_key),
                callback_data=cb_data,
            )
        )
    builder.add(
        InlineKeyboardButton(
            text=i18n.btn.back(),
            callback_data="form_back",
        )
    )
    builder.adjust(2)
    return builder.as_markup()


def build_form_step3_keyboard(
    i18n: TranslatorRunner,
) -> InlineKeyboardMarkup:
    """Step 4: text reply expected; only Back is shown."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=i18n.btn.back(),
            callback_data="form_back",
        )
    )
    builder.adjust(2)
    return builder.as_markup()
