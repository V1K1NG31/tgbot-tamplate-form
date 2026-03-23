"""Offline E2E flows: ``feed_update`` through real routers and scenes."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from aiogram.types import CallbackQuery, Chat, Message, Update, User

from src.core.config import settings
from tests.e2e.app_builder import E2EApp

E2E_USER_ID = 71001
E2E_CHAT_ID = 71001


def _i18n(app: E2EApp):
    return app.hub.get_translator_by_locale("en")


def _bot_surface_message(
    app: E2EApp,
    *,
    message_id: int,
    text: str,
) -> Message:
    payload = {
        "message_id": message_id,
        "date": int(datetime.now(UTC).timestamp()),
        "chat": {"id": E2E_CHAT_ID, "type": "private"},
        "text": text,
    }
    return Message.model_validate(payload, context={"bot": app.bot})


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_e2e_start_sends_welcome_and_menu(e2e_app: E2EApp) -> None:
    i18n = _i18n(e2e_app)
    user = User(id=E2E_USER_ID, is_bot=False, first_name="E2E")
    chat = Chat(id=E2E_CHAT_ID, type="private")
    msg_in = Message(
        message_id=1,
        date=datetime.now(UTC),
        chat=chat,
        from_user=user,
        text="/start",
    )
    upd = Update.model_validate(
        Update(update_id=1, message=msg_in).model_dump(),
        context={"bot": e2e_app.bot},
    )
    await e2e_app.dp.feed_update(
        e2e_app.bot,
        upd,
        translator_hub=e2e_app.hub,
    )
    sends = [
        c
        for c in e2e_app.session.calls
        if c.get("api") == "SendMessage" and c.get("chat_id") == E2E_CHAT_ID
    ]
    assert sends, "expected SendMessage to user chat"
    assert sends[0]["text"] == i18n.start.message()


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_e2e_menu_section_edits_message(e2e_app: E2EApp) -> None:
    i18n = _i18n(e2e_app)
    user = User(id=E2E_USER_ID, is_bot=False, first_name="E2E")
    chat = Chat(id=E2E_CHAT_ID, type="private")

    async def feed_start() -> None:
        msg_in = Message(
            message_id=1,
            date=datetime.now(UTC),
            chat=chat,
            from_user=user,
            text="/start",
        )
        upd = Update.model_validate(
            Update(update_id=1, message=msg_in).model_dump(),
            context={"bot": e2e_app.bot},
        )
        await e2e_app.dp.feed_update(
            e2e_app.bot,
            upd,
            translator_hub=e2e_app.hub,
        )

    async def feed_callback(data: str, base: Message, uid: int) -> None:
        cq = CallbackQuery(
            id=str(uid),
            from_user=user,
            chat_instance="e2e",
            message=base,
            data=data,
        )
        upd = Update.model_validate(
            Update(update_id=uid, callback_query=cq).model_dump(),
            context={"bot": e2e_app.bot},
        )
        await e2e_app.dp.feed_update(
            e2e_app.bot,
            upd,
            translator_hub=e2e_app.hub,
        )

    await feed_start()
    bot_msg = _bot_surface_message(
        e2e_app,
        message_id=1,
        text=i18n.start.message(),
    )
    await feed_callback("menu_what", bot_msg, uid=2)

    edits = [c for c in e2e_app.session.calls if c.get("api") == "EditMessageText"]
    assert edits, "expected EditMessageText for menu section"
    assert edits[-1]["text"] == i18n.get("menu-what")


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_e2e_form_submits_to_admin_and_success_reply(
    e2e_app: E2EApp,
) -> None:
    i18n = _i18n(e2e_app)
    user = User(
        id=E2E_USER_ID,
        is_bot=False,
        first_name="E2E",
        username="e2e_user",
    )
    chat = Chat(id=E2E_CHAT_ID, type="private")
    update_id = 0

    async def feed_message(text: str, incoming_mid: int) -> None:
        nonlocal update_id
        update_id += 1
        msg_in = Message(
            message_id=incoming_mid,
            date=datetime.now(UTC),
            chat=chat,
            from_user=user,
            text=text,
        )
        upd = Update.model_validate(
            Update(update_id=update_id, message=msg_in).model_dump(),
            context={"bot": e2e_app.bot},
        )
        await e2e_app.dp.feed_update(
            e2e_app.bot,
            upd,
            translator_hub=e2e_app.hub,
        )

    async def feed_callback(data: str, base: Message) -> None:
        nonlocal update_id
        update_id += 1
        cq = CallbackQuery(
            id=str(update_id),
            from_user=user,
            chat_instance="e2e",
            message=base,
            data=data,
        )
        upd = Update.model_validate(
            Update(update_id=update_id, callback_query=cq).model_dump(),
            context={"bot": e2e_app.bot},
        )
        await e2e_app.dp.feed_update(
            e2e_app.bot,
            upd,
            translator_hub=e2e_app.hub,
        )

    await feed_message("/start", incoming_mid=1)
    cur = _bot_surface_message(e2e_app, message_id=1, text="placeholder")
    for data in (
        "menu_form",
        "form_individual",
        "form_debt_up300",
        "form_arrears_1m",
    ):
        await feed_callback(data, cur)

    await feed_message("final contact line", incoming_mid=2)

    admin_sends = [
        c
        for c in e2e_app.session.calls
        if c.get("api") == "SendMessage"
        and c.get("chat_id") == settings.admin_chat_id
    ]
    assert len(admin_sends) == 1
    assert "final contact line" in admin_sends[0]["text"]
    assert "@e2e_user" in admin_sends[0]["text"]

    user_sends = [
        c
        for c in e2e_app.session.calls
        if c.get("api") == "SendMessage"
        and c.get("chat_id") == E2E_CHAT_ID
    ]
    assert len(user_sends) >= 2
    assert user_sends[-1]["text"] == i18n.form.success()
