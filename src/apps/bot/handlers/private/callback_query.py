
import logging

from datetime import date
from aiogram import F, Router
from aiogram.types import CallbackQuery

from apps.bot.utils import message_edit_text_keyboard
from apps.bot.keyboards.callback_data import reply_calendar_keyboard, reply_start_keyboard


callback_query_router = Router()
logger = logging.getLogger(__name__)


@callback_query_router.callback_query(F.data == "start_menu")
async def echo_handler(callback: CallbackQuery) -> None:
    await message_edit_text_keyboard(
        obj=callback,
        text=f'Привет {callback.from_user.first_name}! Выбери действие',
        reply_markup=reply_start_keyboard()
    )


@callback_query_router.callback_query(F.data == "calendar")
async def echo_handler(callback: CallbackQuery) -> None:
    year = date.today().year
    mouth = date.today().month

    str_mouth = str(mouth)
    if len(str_mouth) != 2:
        str_mouth = f'0{mouth}'

    await message_edit_text_keyboard(
        obj=callback,
        text=f'Выбери день для редактирования\n{year}-{str_mouth}',
        reply_markup=reply_calendar_keyboard()
    )


@callback_query_router.callback_query(F.data.startswith("calendar/next"))
async def echo_handler(callback: CallbackQuery) -> None:
    data = callback.data.split('/')[2].split('-')
    year = int(data[0])
    mouth = int(data[1]) + 1

    if mouth == 13:
        year += 1
        mouth = 1

    str_mouth = str(mouth)
    if len(str_mouth) != 2:
        str_mouth = f'0{mouth}'

    await message_edit_text_keyboard(
        obj=callback,
        text=f'Выбери день для редактирования\n{year}-{str_mouth}',
        reply_markup=reply_calendar_keyboard(year, mouth)
    )


@callback_query_router.callback_query(F.data.startswith("calendar/back"))
async def echo_handler(callback: CallbackQuery) -> None:
    data = callback.data.split('/')[2].split('-')
    year = int(data[0])
    mouth = int(data[1]) - 1

    if mouth == 0:
        year -= 1
        mouth = 12

    str_mouth = str(mouth)
    if len(str_mouth) != 2:
        str_mouth = f'0{mouth}'

    await message_edit_text_keyboard(
        obj=callback,
        text=f'Выбери день для редактирования\n{year}-{str_mouth}',
        reply_markup=reply_calendar_keyboard(year, mouth)
    )
