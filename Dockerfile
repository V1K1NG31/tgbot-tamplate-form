# ── build ──
FROM python:3.12-slim AS builder

WORKDIR /build

# PyInstaller on Linux needs objdump (binutils)
RUN apt-get update \
    && apt-get install -y --no-install-recommends binutils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry pyinstaller

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

COPY app/ app/

# Bot under app/, package src via --paths=app.
# Bundle locales/ for runtime (en.ftl).
RUN pyinstaller \
    --onefile \
    --name tgbot-template-form \
    --paths=app \
    --add-data "app/locales:locales" \
    --hidden-import=src \
    app/main.py

# ── runtime (тот же базовый образ, что и builder — совместимая glibc) ──
FROM python:3.12-slim

RUN groupadd --system bot \
    && useradd --system --gid bot --no-create-home bot

COPY --from=builder /build/dist/tgbot-template-form \
    /usr/local/bin/tgbot-template-form
# Locales are inside the bundle (--add-data).
# Config: BOT_TOKEN, ADMIN_IDS, ADMIN_CHAT_ID from the environment.
# Example: docker run --env-file .env tgbot-template-form:latest

USER bot

CMD ["tgbot-template-form"]
