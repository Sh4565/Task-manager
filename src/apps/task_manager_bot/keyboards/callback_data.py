
import pytz
import logging
import calendar

from datetime import datetime
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from apps.task_manager_bot.language import get_language


logger = logging.getLogger(__name__)


def reply_start_keyboard(language: str) -> InlineKeyboardMarkup:

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_language('reply_start_keyboard_1', language),
                callback_data='calendar'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('reply_start_keyboard_2', language),
                callback_data=f'calendar/day/{datetime.now().strftime("%Y-%m-%d")}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('reply_start_keyboard_3', language),
                callback_data='profile'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('reply_start_keyboard_4', language),
                callback_data='main_menu'
            )
        ],
    ])

    return keyboard_markup


def reply_calendar_keyboard(language: str, year=None, month=None) -> InlineKeyboardMarkup:
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

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        *calendar_buttons,
        [
            InlineKeyboardButton(text='<-', callback_data=f'calendar/back/{year}-{month}'),
            InlineKeyboardButton(text='->', callback_data=f'calendar/next/{year}-{month}'),
        ],
        [
            InlineKeyboardButton(
                text=get_language('back', language),
                callback_data='start_menu'
            )
        ]
    ])

    return keyboard_markup


def reply_check_day_keyboard(date: str, language: str) -> InlineKeyboardMarkup:
    date = date.split('-')

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_language('reply_check_day_keyboard_1', language),
                callback_data=f'calendar/day/add_task/title/{date[0]}-{date[1]}-{date[2]}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('reply_check_day_keyboard_2', language),
                callback_data=f'calendar/day/list_edit_task/{date[0]}-{date[1]}-{date[2]}/1')
        ],
        [
            InlineKeyboardButton(
                text=get_language('reply_check_day_keyboard_3', language),
                callback_data=f'calendar/day/list_del_task/{date[0]}-{date[1]}-{date[2]}/1')
        ],
        [
            InlineKeyboardButton(
                text=get_language('back', language),
                callback_data=f'calendar/date/{date[0]}-{date[1]}-{date[2]}')
        ]
    ])

    return keyboard_markup


def reply_tasks_day_keyboard(date: str, language: str) -> InlineKeyboardMarkup:
    date = date.split('-')

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_language('back', language),
                callback_data=f'calendar/day/{date[0]}-{date[1]}-{date[2]}'
            )
        ]
    ])

    return keyboard_markup


def reply_return_add_task_keyboard(date: str, language: str) -> InlineKeyboardMarkup:
    date = date.split('-')
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_language('back', language),
                callback_data=f'calendar/day/add_task/edit_title/{date[0]}-{date[1]}-{date[2]}'
            )
        ]
    ])

    return keyboard_markup


def reply_edit_title_keyboard(date: str, data: dict, language: str) -> InlineKeyboardMarkup:
    date = date.split('-')
    try:
        if data['description']:
            pass
        keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_language('next', language),
                    callback_data=f'calendar/day/add_task/edit_description/'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_language('back', language),
                    callback_data=f'calendar/day/{date[0]}-{date[1]}-{date[2]}'
                )
            ]
        ])

        return keyboard_markup

    except KeyError:
        keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_language('next', language),
                    callback_data=f'calendar/day/add_task/description/'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_language('back', language),
                    callback_data=f'calendar/date/{date[0]}-{date[1]}-{date[2]}'
                )
            ]
        ])

        return keyboard_markup


def reply_return_edit_description_keyboard(language: str) -> InlineKeyboardMarkup:
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_language('back', language),
                callback_data=f'calendar/day/add_task/edit_description/'
            )
        ]
    ])

    return keyboard_markup


def reply_edit_description_keyboard(date: str, data: dict, language: str) -> InlineKeyboardMarkup:
    date = date.split('-')

    try:
        if data['time']:
            pass

        keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_language('next', language),
                    callback_data=f'calendar/day/add_task/edit_time/'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_language('back', language),
                    callback_data=f'calendar/day/add_task/edit_title/{date[0]}-{date[1]}-{date[2]}'
                )
            ]
        ])

        return keyboard_markup

    except KeyError:
        keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_language('next', language),
                    callback_data=f'calendar/day/add_task/time/'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_language('back', language),
                    callback_data=f'calendar/day/add_task/edit_title/{date[0]}-{date[1]}-{date[2]}'
                )
            ]
        ])

        return keyboard_markup


def reply_edit_time_keyboard(language: str) -> InlineKeyboardMarkup:

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_language('next', language),
                callback_data=f'calendar/day/add_task/task/'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('back', language),
                callback_data=f'calendar/day/add_task/edit_description/'
            )
        ]
    ])

    return keyboard_markup


def reply_check_task_keyboard(date: str, language: str) -> InlineKeyboardMarkup:
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_language('reply_check_task_keyboard_1', language),
                callback_data=f'calendar/day/add_task/save'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('reply_check_task_keyboard_2', language),
                callback_data=f'calendar/day/add_task/edit_title/{date}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('reply_check_task_keyboard_3', language),
                callback_data=f'calendar/date/{date}'
            )
        ],
    ])

    return keyboard_markup


def reply_list_task_keyboard(language: str, date: str, list_tasks: list, parameter: str, page: int = 1) -> InlineKeyboardMarkup:
    tasks_per_page = 5
    start_index = (page - 1) * tasks_per_page
    end_index = start_index + tasks_per_page
    current_tasks = list_tasks[start_index:end_index]

    keyboard_buttons = []

    for task in current_tasks:
        start_time = task.start_datetime.strftime("%H:%M")
        end_time = task.end_datetime.strftime("%H:%M")
        task_button = InlineKeyboardButton(
            text=f'{start_time}-{end_time} {task.title}',
            callback_data=f'calendar/day/{parameter}/{task.id}'
        )
        keyboard_buttons.append([task_button])

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='<-',
                callback_data=f'calendar/day/list_{parameter}/{date}/{page - 1}')
        )
    if end_index < len(list_tasks):
        navigation_buttons.append(
            InlineKeyboardButton(
                text='->',
                callback_data=f'calendar/day/list_{parameter}/{date}/{page + 1}')
        )

    if navigation_buttons:
        keyboard_buttons.append(navigation_buttons)

    keyboard_buttons.append([
        InlineKeyboardButton(
            text=get_language('back', language),
            callback_data=f'calendar/day/{date}'
        )
    ])

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard_markup


def enter_to_delete(date: str, task_id: int, language: str) -> InlineKeyboardMarkup:

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_language('yes', language),
                callback_data=f'calendar/day/enter_del_task/{task_id}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('no', language),
                callback_data=f'calendar/day/{date}'
            )
        ]
    ])

    return keyboard_markup


def enter_to_successful_task(task_id: int, language: str) -> InlineKeyboardMarkup:
    task_id = str(task_id)

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_language('yes', language),
                callback_data=f'successful_task/True/{task_id}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('no', language),
                callback_data=f'successful_task/False/{task_id}'
            )
        ]
    ])

    return keyboard_markup


def reply_list_timezone_keyboard(language: str, page: int = 1) -> InlineKeyboardMarkup:
    per_page = 15
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    timezones = pytz.all_timezones
    chunk_timezones = timezones[start_index:end_index]

    keyboard_buttons = []

    for timezone in chunk_timezones:

        timezone_button = InlineKeyboardButton(
            text=timezone,
            callback_data=f'set_timezone/{timezone.replace("/", "-")}'
        )
        keyboard_buttons.append([timezone_button])

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='<-',
                callback_data=f'set_list_timezones/{page - 1}')
        )
    if end_index < len(timezones):
        navigation_buttons.append(
            InlineKeyboardButton(
                text='->',
                callback_data=f'set_list_timezones/{page + 1}')
        )

    if navigation_buttons:
        keyboard_buttons.append(navigation_buttons)

    keyboard_buttons.append([
        InlineKeyboardButton(
            text=get_language('back', language),
            callback_data=f'profile'
        )
    ])

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard_markup


def profile_keyboard(language: str) -> InlineKeyboardMarkup:

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_language('profile_keyboard_1', language),
                callback_data=f'set_list_timezones/1'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('profile_keyboard_2', language),
                callback_data=f'choice_language'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('back', language),
                callback_data=f'start_menu'
            )
        ]
    ])

    return keyboard_markup


def language_keyboard(language: str) -> InlineKeyboardMarkup:

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_language('language_keyboard_1', language),
                callback_data=f'set_language/en'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('language_keyboard_2', language),
                callback_data=f'set_language/ua'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('language_keyboard_3', language),
                callback_data=f'set_language/ru'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_language('back', language),
                callback_data=f'profile'
            )
        ]
    ])

    return keyboard_markup
