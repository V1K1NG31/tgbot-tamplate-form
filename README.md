# tgbot-template-form

Telegram bot template: **info menu** + **multi-step form** (aiogram 3, Fluent, Redis), with a fictional demo copy you can replace.

Longer summary: [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md).

## Features

- Inline menu sections with editable copy in `app/locales/en.ftl` (English default)
- Form `Scene`: choice steps + free-text contact, notification to `ADMIN_CHAT_ID`
- Redis-backed FSM storage
- Optional Docker image with a PyInstaller one-file binary

## Requirements

- Python **3.12+**
- **Redis** (local or remote URL)
- A Telegram **bot token** from [@BotFather](https://t.me/BotFather)

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

`tests/conftest.py` sets dummy `BOT_TOKEN` and `ADMIN_CHAT_ID` so importing handlers does not require a real `.env`.

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
- `tests/` — pytest suite (Fluent hub, keyboards, config, Telegram helpers)
- `docs/PROJECT_OVERVIEW.md` — short project summary (English)

## License

MIT — see `pyproject.toml`.
