
import logging
import calendar

from datetime import datetime
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup


logger = logging.getLogger(__name__)


def reply_start_keyboard():

    reapply_start_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Календарь', callback_data='calendar')
        ],
        [
            InlineKeyboardButton(text='Распорядок дня', callback_data='main_menu')
        ],
        [
            InlineKeyboardButton(text='Мой профиль', callback_data='main_menu')
        ],
        [
            InlineKeyboardButton(text='Поддержка', callback_data='main_menu')
        ],
    ])

    return reapply_start_buttons


def reply_calendar_keyboard(year=None, month=None):
    cal = calendar.Calendar()

    if not year and not month:
        year = datetime.now().year
        month = datetime.now().month

    calendar_dates = list(cal.itermonthdays3(year, month))

    week_buttons = []
    calendar_buttons = []

    for date in calendar_dates:
        if date[1] == 0:
            week_buttons.append(InlineKeyboardButton(text=" ", callback_data='ignore'))
        else:
            week_buttons.append(InlineKeyboardButton(
                text=str(date[2]),
                callback_data=f'calendar/day/{str(date[0])}-{str(date[1])}-{str(date[2])}')
            )

        if len(week_buttons) == 7:
            calendar_buttons.append(week_buttons)
            week_buttons = []

    if week_buttons:
        calendar_buttons.append(week_buttons)

    reapply_calendar_buttons = InlineKeyboardMarkup(inline_keyboard=[
        *calendar_buttons,
        [
            InlineKeyboardButton(text='<-', callback_data=f'calendar/back/{year}-{month}'),
            InlineKeyboardButton(text='->', callback_data=f'calendar/next/{year}-{month}'),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='start_menu')
        ]
    ])

    return reapply_calendar_buttons
