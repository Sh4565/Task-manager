
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

    reply__calendar_buttons = InlineKeyboardMarkup(inline_keyboard=[
        *calendar_buttons,
        [
            InlineKeyboardButton(text='<-', callback_data=f'calendar/back/{year}-{month}'),
            InlineKeyboardButton(text='->', callback_data=f'calendar/next/{year}-{month}'),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='start_menu')
        ]
    ])

    return reply__calendar_buttons


def reply_check_day_keyboard(date: str):
    date = date.split('-')

    check_day_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Добавить задачу',
                callback_data=f'calendar/day/add_task/title/{date[0]}-{date[1]}-{date[2]}'
            )
        ],
        [
            InlineKeyboardButton(text='Редактировать задачу', callback_data='calendar/day/edit_task')
        ],
        [
            InlineKeyboardButton(text='Удалить задачу', callback_data='calendar/day/del_task')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=f'calendar/date/{date[0]}-{date[1]}-{date[2]}')
        ]
    ])

    return check_day_buttons


def reply_return_calendar_keyboard(date: str):
    date = date.split('-')

    return_calendar_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data=f'calendar/date/{date[0]}-{date[1]}-{date[2]}'
            )
        ]
    ])

    return return_calendar_buttons


def reply_return_add_task_keyboard(date: str):
    date = date.split('-')
    return_add_task_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data=f'calendar/day/add_task/edit_title/{date[0]}-{date[1]}-{date[2]}'
            )
        ]
    ])

    return return_add_task_buttons


def reply_edit_title_keyboard(date: str, data: dict):
    date = date.split('-')
    try:
        if data['description']:
            pass
        return_edit_title_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Далее',
                    callback_data=f'calendar/day/add_task/edit_description/'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Назад',
                    callback_data=f'calendar/date/{date[0]}-{date[1]}-{date[2]}'
                )
            ]
        ])

        return return_edit_title_buttons

    except KeyError:
        return_edit_title_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Далее',
                    callback_data=f'calendar/day/add_task/description/'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Назад',
                    callback_data=f'calendar/date/{date[0]}-{date[1]}-{date[2]}'
                )
            ]
        ])

        return return_edit_title_buttons


def reply_return_edit_description_keyboard():
    return_edit_description_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data=f'calendar/day/add_task/edit_description/'
            )
        ]
    ])

    return return_edit_description_buttons


def reply_edit_description_keyboard(date: str, data: dict):
    date = date.split('-')

    try:
        if data['time']:
            pass

        return_edit_description_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Далее',
                    callback_data=f'calendar/day/add_task/edit_time/'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Назад',
                    callback_data=f'calendar/day/add_task/edit_title/{date[0]}-{date[1]}-{date[2]}'
                )
            ]
        ])
        return return_edit_description_buttons

    except KeyError:
        return_edit_description_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Далее',
                    callback_data=f'calendar/day/add_task/time/'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Назад',
                    callback_data=f'calendar/day/add_task/edit_title/{date[0]}-{date[1]}-{date[2]}'
                )
            ]
        ])

        return return_edit_description_buttons


def reply_edit_time_keyboard():

    return_edit_time_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Далее',
                callback_data=f'calendar/day/add_task/task/'
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data=f'calendar/day/add_task/edit_description/'
            )
        ]
    ])

    return return_edit_time_buttons


def reply_check_task_keyboard(date: str):
    return_edit_description_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Сохранить', callback_data=f'calendar/day/add_task/save/')
        ],
        [
            InlineKeyboardButton(text='Изменить', callback_data=f'calendar/day/add_task/edit_title/{date}')
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data=f'calendar/date/{date}')
        ],
    ])

    return return_edit_description_buttons
