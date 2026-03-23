# Project overview

**What this is:** an open **aiogram 3** Telegram bot template with a main **info menu** (short sections), a multi-step **form** built with `Scene` + FSM, and a summary message sent to an **admin chat**. User-facing copy is **English** in **Fluent** (`app/locales/en.ftl`); dialog state uses **Redis**.

**Why use it:** reuse the router, middleware, keyboard, and form-scene layout, then swap strings, form steps, and branding for your own product. The repo ships a **fictional demo** (“Svetlitsa”) so there are no real services or commitments implied.

**Data flow:** user browses menu sections → optionally completes the form (inline steps + final free-text contact) → the bot posts a summary to `ADMIN_CHAT_ID`. `ADMIN_IDS` is reserved for future admin features; the admin router is currently empty.

**Stack:** Python 3.12+, Pydantic Settings, fluentogram, Redis. The Docker build optionally produces a **PyInstaller** single-file binary named `tgbot-template-form`.
