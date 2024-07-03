
import logging

from datetime import date
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from apps.task_manager_bot.utils.language import get_language
from apps.task_manager_bot.bot.keyboards import callback_data
from apps.task_manager_bot.utils import message_edit_text_keyboard


calendar_router = Router()
logger = logging.getLogger(__name__)


@calendar_router.callback_query(F.data == "calendar")
async def calendar(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()
    year = date.today().year
    mouth = date.today().month

    str_mouth = str(mouth)
    if len(str_mouth) != 2:
        str_mouth = f'0{mouth}'

    text = get_language('calendar', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$DATE', f'{year}-{str_mouth}'),
        reply_markup=callback_data.reply_calendar_keyboard(language_user)
    )


@calendar_router.callback_query(F.data.startswith("calendar/next"))
async def calendar_next(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()
    data = callback.data.split('/')[2].split('-')
    year = int(data[0])
    mouth = int(data[1]) + 1

    if mouth == 13:
        year += 1
        mouth = 1

    str_mouth = str(mouth)
    if len(str_mouth) != 2:
        str_mouth = f'0{mouth}'

    text = get_language('calendar', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$DATE', f'{year}-{str_mouth}'),
        reply_markup=callback_data.reply_calendar_keyboard(language_user, year, mouth)
    )


@calendar_router.callback_query(F.data.startswith("calendar/back"))
async def calendar_back(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()
    data = callback.data.split('/')[2].split('-')
    year = int(data[0])
    mouth = int(data[1]) - 1

    if mouth == 0:
        year -= 1
        mouth = 12

    str_mouth = str(mouth)
    if len(str_mouth) != 2:
        str_mouth = f'0{mouth}'

    text = get_language('calendar', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$DATE', f'{year}-{str_mouth}'),
        reply_markup=callback_data.reply_calendar_keyboard(language_user, year, mouth)
    )


@calendar_router.callback_query(F.data.startswith("calendar/date"))
async def calendar_date(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()
    data = callback.data.split('/')[2].split('-')
    year = int(data[0])
    mouth = int(data[1])

    str_mouth = str(mouth)
    if len(str_mouth) != 2:
        str_mouth = f'0{mouth}'

    text = get_language('calendar', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$DATE', f'{year}-{str_mouth}'),
        reply_markup=callback_data.reply_calendar_keyboard(language_user, year, mouth)
    )
