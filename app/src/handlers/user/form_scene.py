"""Form scene: client type → scope → timeline → contact."""

from typing import Any

from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from src.core.config import settings
from src.core.fluent import get_default_i18n
from src.keyboards.form import (
    ARREARS_OPTIONS,
    DEBT_OPTIONS,
    PERSON_TYPE_OPTIONS,
    build_form_step0_keyboard,
    build_form_step1_keyboard,
    build_form_step2_keyboard,
    build_form_step3_keyboard,
)
from src.keyboards.menu import build_menu_keyboard
from src.utils.telegram import editable_message_from_callback

_PERSON_LABELS = {cb: ftl for ftl, cb in PERSON_TYPE_OPTIONS}
_DEBT_LABELS = {cb: ftl for ftl, cb in DEBT_OPTIONS}
_ARREARS_LABELS = {cb: ftl for ftl, cb in ARREARS_OPTIONS}


class FormScene(Scene, state="form"):  # type: ignore[call-arg]
    """Form scene: client type → scope → timeline → contact."""

    @on.callback_query.enter()
    async def on_enter(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        step: int = 1,
    ) -> Any:
        """
        Enter the form scene:
        step 1: individual or company
        step 2: scope hint
        step 3: desired timeline
        step 4: free-text contact
        """
        await state.update_data(step=step)
        i18n = get_default_i18n()

        if step == 1:
            text = i18n.form.q0()
            markup = build_form_step0_keyboard(i18n)
        elif step == 2:
            text = i18n.form.q1()
            markup = build_form_step1_keyboard(i18n)
        elif step == 3:
            text = i18n.form.q2()
            markup = build_form_step2_keyboard(i18n)
        else:
            text = i18n.form.q3()
            markup = build_form_step3_keyboard(i18n)

        msg = editable_message_from_callback(callback)
        if msg is None:
            await callback.answer()
            return
        await msg.edit_text(text, reply_markup=markup)
        await callback.answer()

    # --- step 1: client type ---

    @on.callback_query(F.data.in_(("form_individual", "form_sole_proprietor")))
    async def on_person_type_selected(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        """Persist individual vs company (state key: person_type)."""
        await state.update_data(person_type=callback.data)
        await self.wizard.retake(step=2)

    # --- step 2: scope ---

    @on.callback_query(F.data.startswith("form_debt_"))
    async def on_debt_selected(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        """Persist scope tier (state key: debt)."""
        await state.update_data(debt=callback.data)
        await self.wizard.retake(step=3)

    # --- step 3: timeline ---

    @on.callback_query(F.data.startswith("form_arrears_"))
    async def on_arrears_selected(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        """Persist timeline choice (state key: arrears)."""
        await state.update_data(arrears=callback.data)
        await self.wizard.retake(step=4)

    # --- step 4: contact ---

    @on.message(F.text)
    async def on_username(
        self,
        message: Message,
        state: FSMContext,
        bot: Bot,
    ) -> None:
        """Free-text contact details."""
        data = await state.get_data()
        i18n = get_default_i18n()
        if data.get("step") != 4:
            return

        raw_text = message.text
        if raw_text is None:
            return
        contact = raw_text.strip()
        person_ftl = _PERSON_LABELS.get(data.get("person_type", ""), "")
        debt_ftl = _DEBT_LABELS.get(data.get("debt", ""), "")
        arrears_ftl = _ARREARS_LABELS.get(data.get("arrears", ""), "")

        user = message.from_user
        if user is None:
            return
        user_link = (
            f"@{user.username}"
            if user.username
            else f'<a href="tg://user?id={user.id}">{user.full_name}</a>'
        )

        admin_text = i18n.form.admin.message(
            person_type=(i18n.get(person_ftl) if person_ftl else "—"),
            debt=i18n.get(debt_ftl) if debt_ftl else "—",
            arrears=i18n.get(arrears_ftl) if arrears_ftl else "—",
            contact=contact,
            user=user_link,
        )
        await bot.send_message(
            chat_id=settings.admin_chat_id,
            text=admin_text,
        )

        await message.answer(
            i18n.form.success(),
            reply_markup=build_menu_keyboard().as_markup(),
        )
        await self.wizard.exit()

    # --- back button ---

    @on.callback_query(F.data == "form_back")
    async def on_back(
        self,
        _callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        """Go to previous step or exit the scene."""
        data = await state.get_data()
        step = data.get("step", 1)

        if step <= 1:
            await self.wizard.exit()
        else:
            await self.wizard.retake(step=step - 1)

    # --- exit scene → main menu ---

    @on.callback_query.exit()
    async def on_exit(
        self,
        callback: CallbackQuery,
    ) -> None:
        """On scene exit, show the main menu."""
        i18n = get_default_i18n()
        msg = editable_message_from_callback(callback)
        if msg is None:
            await callback.answer()
            return
        await msg.edit_text(
            i18n.start.message(),
            reply_markup=build_menu_keyboard().as_markup(),
        )
        await callback.answer()
