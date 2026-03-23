"""Tests for ``FormScene`` handlers (mock wizard + hub)."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram.types import User

import src.core.fluent as fluent
from src.core.config import settings
from src.handlers.user.form_scene import FormScene


@pytest.fixture
def scene_wizard() -> MagicMock:
    """Minimal wizard with async navigation hooks."""
    w = MagicMock()
    w.retake = AsyncMock()
    w.exit = AsyncMock()
    return w


@pytest.fixture
def default_hub(translator_hub):
    """Install default hub for ``get_default_i18n``; restore slot after."""
    previous = fluent._hub_slot[0]
    fluent.set_default_hub(translator_hub)
    yield translator_hub
    fluent._hub_slot[0] = previous


@pytest.mark.parametrize(
    ("step", "text_attr"),
    [
        (1, "q0"),
        (2, "q1"),
        (3, "q2"),
        (4, "q3"),
    ],
)
@pytest.mark.asyncio
async def test_on_enter_edits_message_per_step(
    default_hub,
    scene_wizard,
    i18n,
    step: int,
    text_attr: str,
) -> None:
    state = MagicMock()
    state.update_data = AsyncMock()
    callback = MagicMock()
    callback.answer = AsyncMock()
    msg = MagicMock()
    msg.edit_text = AsyncMock()
    with patch(
        "src.handlers.user.form_scene.editable_message_from_callback",
        return_value=msg,
    ):
        scene = FormScene(scene_wizard)
        await scene.on_enter(callback, state, step=step)
    state.update_data.assert_awaited_once_with(step=step)
    msg.edit_text.assert_awaited_once()
    expected = getattr(i18n.form, text_attr)()
    assert msg.edit_text.call_args[0][0] == expected
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_on_enter_no_editable_message_only_answers(
    default_hub,
    scene_wizard,
) -> None:
    state = MagicMock()
    state.update_data = AsyncMock()
    callback = MagicMock()
    callback.answer = AsyncMock()
    with patch(
        "src.handlers.user.form_scene.editable_message_from_callback",
        return_value=None,
    ):
        scene = FormScene(scene_wizard)
        await scene.on_enter(callback, state, step=1)
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_on_person_type_selected_updates_state_and_retake(
    scene_wizard,
) -> None:
    state = MagicMock()
    state.update_data = AsyncMock()
    callback = MagicMock()
    callback.data = "form_individual"
    scene = FormScene(scene_wizard)
    await scene.on_person_type_selected(callback, state)
    state.update_data.assert_awaited_once_with(person_type="form_individual")
    scene_wizard.retake.assert_awaited_once_with(step=2)


@pytest.mark.asyncio
async def test_on_debt_selected_updates_state_and_retake(scene_wizard) -> None:
    state = MagicMock()
    state.update_data = AsyncMock()
    callback = MagicMock()
    callback.data = "form_debt_up300"
    scene = FormScene(scene_wizard)
    await scene.on_debt_selected(callback, state)
    state.update_data.assert_awaited_once_with(debt="form_debt_up300")
    scene_wizard.retake.assert_awaited_once_with(step=3)


@pytest.mark.asyncio
async def test_on_arrears_selected_updates_state_and_retake(
    scene_wizard,
) -> None:
    state = MagicMock()
    state.update_data = AsyncMock()
    callback = MagicMock()
    callback.data = "form_arrears_1m"
    scene = FormScene(scene_wizard)
    await scene.on_arrears_selected(callback, state)
    state.update_data.assert_awaited_once_with(arrears="form_arrears_1m")
    scene_wizard.retake.assert_awaited_once_with(step=4)


@pytest.mark.asyncio
async def test_on_username_returns_when_text_none(
    default_hub,
    scene_wizard,
) -> None:
    state = MagicMock()
    state.get_data = AsyncMock(
        return_value={
            "step": 4,
            "person_type": "form_individual",
            "debt": "form_debt_up300",
            "arrears": "form_arrears_1m",
        }
    )
    message = MagicMock()
    message.text = None
    message.from_user = User(id=1, is_bot=False, first_name="A")
    bot = MagicMock()
    bot.send_message = AsyncMock()
    scene = FormScene(scene_wizard)
    await scene.on_username(message, state, bot)
    bot.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_on_username_returns_when_from_user_none(
    default_hub,
    scene_wizard,
) -> None:
    state = MagicMock()
    state.get_data = AsyncMock(
        return_value={
            "step": 4,
            "person_type": "form_individual",
            "debt": "form_debt_up300",
            "arrears": "form_arrears_1m",
        }
    )
    message = MagicMock()
    message.text = "hi"
    message.from_user = None
    bot = MagicMock()
    bot.send_message = AsyncMock()
    scene = FormScene(scene_wizard)
    await scene.on_username(message, state, bot)
    bot.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_on_username_skips_when_step_not_four(
    default_hub,
    scene_wizard,
) -> None:
    state = MagicMock()
    state.get_data = AsyncMock(return_value={"step": 1})
    message = MagicMock()
    message.text = "hello"
    bot = MagicMock()
    bot.send_message = AsyncMock()
    scene = FormScene(scene_wizard)
    await scene.on_username(message, state, bot)
    bot.send_message.assert_not_called()
    scene_wizard.exit.assert_not_called()


@pytest.mark.asyncio
async def test_on_username_submits_to_admin_and_exits(
    default_hub,
    scene_wizard,
    i18n,
) -> None:
    state = MagicMock()
    state.get_data = AsyncMock(
        return_value={
            "step": 4,
            "person_type": "form_individual",
            "debt": "form_debt_up300",
            "arrears": "form_arrears_1m",
        }
    )
    user = User(id=7, is_bot=False, first_name="Test", username="tester")
    message = MagicMock()
    message.text = "  reach me here  "
    message.from_user = user
    message.answer = AsyncMock()
    bot = MagicMock()
    bot.send_message = AsyncMock()
    scene = FormScene(scene_wizard)
    await scene.on_username(message, state, bot)
    bot.send_message.assert_awaited_once()
    assert bot.send_message.call_args.kwargs["chat_id"] == settings.admin_chat_id
    admin_text = bot.send_message.call_args.kwargs["text"]
    assert "reach me here" in admin_text
    assert "@tester" in admin_text
    message.answer.assert_awaited_once()
    assert message.answer.call_args[0][0] == i18n.form.success()
    scene_wizard.exit.assert_awaited_once()


@pytest.mark.asyncio
async def test_on_back_exits_when_step_one(scene_wizard) -> None:
    state = MagicMock()
    state.get_data = AsyncMock(return_value={"step": 1})
    callback = MagicMock()
    scene = FormScene(scene_wizard)
    await scene.on_back(callback, state)
    scene_wizard.exit.assert_awaited_once()
    scene_wizard.retake.assert_not_called()


@pytest.mark.asyncio
async def test_on_back_retakes_previous_step(scene_wizard) -> None:
    state = MagicMock()
    state.get_data = AsyncMock(return_value={"step": 3})
    callback = MagicMock()
    scene = FormScene(scene_wizard)
    await scene.on_back(callback, state)
    scene_wizard.retake.assert_awaited_once_with(step=2)
    scene_wizard.exit.assert_not_called()


@pytest.mark.asyncio
async def test_on_exit_shows_main_menu(default_hub, scene_wizard, i18n) -> None:
    callback = MagicMock()
    callback.answer = AsyncMock()
    msg = MagicMock()
    msg.edit_text = AsyncMock()
    with patch(
        "src.handlers.user.form_scene.editable_message_from_callback",
        return_value=msg,
    ):
        scene = FormScene(scene_wizard)
        await scene.on_exit(callback)
    msg.edit_text.assert_awaited_once()
    assert msg.edit_text.call_args[0][0] == i18n.start.message()
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_on_exit_no_message_only_answers(
    default_hub,
    scene_wizard,
) -> None:
    callback = MagicMock()
    callback.answer = AsyncMock()
    with patch(
        "src.handlers.user.form_scene.editable_message_from_callback",
        return_value=None,
    ):
        scene = FormScene(scene_wizard)
        await scene.on_exit(callback)
    callback.answer.assert_awaited_once()
