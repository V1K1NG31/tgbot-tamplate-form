"""Fluent-based localization."""

import sys
from pathlib import Path

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub, TranslatorRunner

# In a PyInstaller bundle, locale files live under sys._MEIPASS/locales.
_hub_slot: list[TranslatorHub | None] = [None]


def set_default_hub(hub: TranslatorHub) -> None:
    """
    Set the default hub (call from main after create_translator_hub).
    """
    _hub_slot[0] = hub


def get_default_i18n() -> TranslatorRunner:
    """
    Return the runner for locale ``en`` (e.g. scenes without middleware data).
    """
    hub = _hub_slot[0]
    if hub is None:
        raise RuntimeError(
            "translator hub not set; call set_default_hub() in main"
        )
    return hub.get_translator_by_locale("en")


# Dev: app/locales; frozen: _MEIPASS/locales (PyInstaller).
if getattr(sys, "frozen", False):
    _MEIPASS_RAW = getattr(sys, "_MEIPASS", None)
    if not isinstance(_MEIPASS_RAW, str):
        raise RuntimeError(
            "frozen build: sys._MEIPASS is missing or not a path"
        )
    _BASE = Path(_MEIPASS_RAW)
else:
    _BASE = Path(__file__).resolve().parents[2]
_LOCALES_DIR = _BASE / "locales"


def create_translator_hub() -> TranslatorHub:
    """Build a TranslatorHub from locales/en.ftl (English, default locale)."""
    en_ftl = (_LOCALES_DIR / "en.ftl").read_text(encoding="utf-8")
    return TranslatorHub(
        locales_map={"en": ("en",)},
        translators=[
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_string(
                    "en-US",
                    en_ftl,
                    use_isolating=False,
                ),
            ),
        ],
        root_locale="en",
    )
