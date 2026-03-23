"""Load ``.env.test`` before ``src.core.config`` is imported (pytest only)."""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

_root = Path(__file__).resolve().parents[1]
_env_test = _root / ".env.test"
if not _env_test.is_file():
    msg = (
        "Missing .env.test at repository root "
        f"({_env_test}). Copy from .env.test.example or restore from VCS."
    )
    raise FileNotFoundError(msg)
load_dotenv(_env_test, override=False)
