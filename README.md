# tgbot-template-form

Telegram bot template: **info menu** + **multi-step form** (aiogram 3, Fluent, Redis), with a fictional demo copy you can replace.

Longer summary: [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md).

## Features

- Inline menu sections with editable copy in `app/locales/en.ftl` (English default)
- Form `Scene`: choice steps + free-text contact, notification to `ADMIN_CHAT_ID`
- Redis-backed FSM storage
- Optional Docker image with a PyInstaller one-file binary

## Requirements

- Python **3.12–3.14** (aiogram currently declares `python <3.15`)
- **Redis** (local or remote URL)
- A Telegram **bot token** from [@BotFather](https://t.me/BotFather)

After pulling dependency updates, run `poetry lock` (if the lockfile changed) and `poetry install` so `pydantic-core` and `aiohttp` match your interpreter (prebuilt wheels exist for 3.12–3.14).

## Configuration

Copy `.env.example` to `.env` and set:

| Variable         | Description |
|------------------|-------------|
| `BOT_TOKEN`      | Telegram bot token |
| `ADMIN_CHAT_ID`  | Chat ID where form submissions are sent (e.g. supergroup with bot) |
| `ADMIN_IDS`      | JSON array of admin user IDs (optional; reserved for future use), e.g. `[123456789]` |
| `REDIS_URL`      | Redis URL, default `redis://localhost:6379/0` |

## Run locally

From the repository root:

```bash
poetry install
cp .env.example .env
# edit .env
PYTHONPATH=app python app/main.py
```

Ensure Redis is running if you use the default `REDIS_URL`.

## Tests

```bash
poetry install --with dev
PYTHONPATH=app poetry run pytest
```

Coverage (package `app/src` only; entrypoint `app/main.py` is not imported by tests):

```bash
PYTHONPATH=app poetry run pytest --cov --cov-report=term-missing
```

Pytest loads **only** **`.env.test`** (tracked in this template with safe fake values). **`.env.test.example`** is a non-runtime copy you can use as a checklist or when setting up another checkout.

**E2E (offline):** full dispatcher + scenes, no HTTP to Telegram — fake API session records `SendMessage` / `EditMessageText` / `AnswerCallbackQuery`:

```bash
poetry run pytest -m e2e
```

If you see `ModuleNotFoundError: No module named 'pydantic_core'`, the environment is incomplete: run `poetry install` from the project root (or recreate the venv). On **Python 3.14**, use the lockfile versions in this repo (`pydantic` 2.12.x + `aiohttp` 3.13.x) so wheels install instead of failed local builds.

## Docker

```bash
cp .env.example .env
# edit .env — BOT_TOKEN, ADMIN_CHAT_ID, ADMIN_IDS as needed
docker compose --env-file .env up --build
```

The app service is named **`bot`**. Redis is included in the compose file.

## Layout

- `app/main.py` — entrypoint, dispatcher, Redis storage, scene registry
- `app/src/` — handlers, keyboards, middlewares, config
- `app/locales/en.ftl` — Fluent strings (replace demo “Svetlitsa” copy with yours)
- `.env.test` — variables for pytest; `.env.test.example` is documentation only
- `tests/` — pytest suite (Fluent hub, keyboards, config, Telegram helpers, `tests/e2e/` offline dispatcher tests)
- `docs/PROJECT_OVERVIEW.md` — short project summary (English)

## License

MIT — see `pyproject.toml`.
