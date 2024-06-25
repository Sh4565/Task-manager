
import logging

from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from .menus import profile
from apps.task_manager_bot.db import user_methods
from apps.task_manager_bot.utils.language import get_language
from apps.task_manager_bot.bot.keyboards import callback_data
from apps.task_manager_bot.utils import message_edit_text_keyboard


settings_user_router = Router()
logger = logging.getLogger(__name__)


@settings_user_router.callback_query(F.data.startswith("set_list_timezones"))
async def set_list_timezones(callback: CallbackQuery,
                             state: FSMContext, language_user: str) -> None:
    await state.clear()

    page = int(callback.data.split('/')[1])

    text = get_language('set_list_timezones', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_list_timezone_keyboard(language_user, page)
    )


@settings_user_router.callback_query(F.data.startswith("set_timezone"))
async def set_timezone(callback: CallbackQuery,
                       state: FSMContext, bot: Bot, language_user: str) -> None:
    await state.clear()
    timezone = callback.data.split('/')[1].replace('-', '/')

    await user_methods.update_user(callback.from_user, timezone=timezone)
    text = get_language('set_timezone', language_user)
    text = text.replace('$TIMEZONE', timezone)
    await callback.answer(text)
    await bot.answer_callback_query(callback.id)
    await profile(callback, state, language_user)


@settings_user_router.callback_query(F.data.startswith("choice_language"))
async def choice_language(callback: CallbackQuery,
                          state: FSMContext, language_user: str) -> None:
    await state.clear()

    text = get_language('choice_language', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.language_keyboard(language_user)
    )


@settings_user_router.callback_query(F.data.startswith("set_language"))
async def set_language(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    language = callback.data.split('/')[1]

    await user_methods.update_user(callback.from_user, language=language)
    await profile(callback, state, language)

