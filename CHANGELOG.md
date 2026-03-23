# Changelog

User-visible changes for bot operators and template users.
Internal-only refactors are omitted.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Latest release at the **top**.

## [Unreleased]

Move items here while developing; cut a dated release when you publish.

### Added

- Root `README.md` and `docs/PROJECT_OVERVIEW.md`.
- Pytest suite under `tests/` (keyboards, Fluent, settings, Telegram utils).
- Tests for i18n middleware, `/start`, menu handlers (detail and plain branches,
  guard paths), and the multi-step `FormScene`.
- Offline E2E tests (`pytest -m e2e`): `Dispatcher.feed_update` with in-memory FSM
  and a fake Telegram API session (`tests/e2e/`).
- Dev dependency `pytest-cov` and `[tool.coverage.*]` in `pyproject.toml` for optional `pytest --cov`.

### Changed

- Pytest: env vars load **only** from `.env.test` via `python-dotenv` and
  `tests/_bootstrap_env.py`; `.env.test.example` is a non-runtime template.
- Dependencies for **Python 3.14**: `aiogram` ≥3.26, `pydantic` 2.12.x (with `pydantic-core` wheels), `aiohttp` 3.13.x (wheels for 3.14). Declared `requires-python` as `>=3.12,<3.15` (matches aiogram).
- Demo copy and menu labels: fictional brand “Svetlitsa”, no bankruptcy niche.
- Package and Docker artifacts: `tgbot-template-form` instead of `bfl`; compose service `bot`.
- **English-only UI:** default locale `en`, strings in `app/locales/en.ftl`; code comments and docs in English.

---

## [0.1.0] — 2026-03-22

### Added

- Changelog file.
