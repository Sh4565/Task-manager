
import logging
import calendar

from datetime import datetime
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup


logger = logging.getLogger(__name__)


def reply_start_keyboard() -> InlineKeyboardMarkup:

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Календарь', callback_data='calendar')
        ],
        [
            InlineKeyboardButton(text='Распорядок дня', callback_data=f'calendar/day/{datetime.now().strftime("%Y-%m-%d")}')
        ],
        [
            InlineKeyboardButton(text='Мой профиль', callback_data='main_menu')
        ],
        [
            InlineKeyboardButton(text='Поддержка', callback_data='main_menu')
        ],
    ])

    return keyboard_markup


def reply_calendar_keyboard(year=None, month=None) -> InlineKeyboardMarkup:
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
            InlineKeyboardButton(text='Назад', callback_data='start_menu')
        ]
    ])

    return keyboard_markup


def reply_check_day_keyboard(date: str) -> InlineKeyboardMarkup:
    date = date.split('-')

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Добавить задачу',
                callback_data=f'calendar/day/add_task/title/{date[0]}-{date[1]}-{date[2]}'
            )
        ],
        [
            InlineKeyboardButton(
                text='Редактировать задачу',
                callback_data=f'calendar/day/list_edit_task/{date[0]}-{date[1]}-{date[2]}/1')
        ],
        [
            InlineKeyboardButton(
                text='Удалить задачу',
                callback_data=f'calendar/day/list_del_task/{date[0]}-{date[1]}-{date[2]}/1')
        ],
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data=f'calendar/date/{date[0]}-{date[1]}-{date[2]}')
        ]
    ])

    return keyboard_markup


def reply_tasks_day_keyboard(date: str) -> InlineKeyboardMarkup:
    date = date.split('-')

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data=f'calendar/day/{date[0]}-{date[1]}-{date[2]}'
            )
        ]
    ])

    return keyboard_markup


def reply_return_add_task_keyboard(date: str) -> InlineKeyboardMarkup:
    date = date.split('-')
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data=f'calendar/day/add_task/edit_title/{date[0]}-{date[1]}-{date[2]}'
            )
        ]
    ])

    return keyboard_markup


def reply_edit_title_keyboard(date: str, data: dict) -> InlineKeyboardMarkup:
    date = date.split('-')
    try:
        if data['description']:
            pass
        keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Далее',
                    callback_data=f'calendar/day/add_task/edit_description/'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Назад',
                    callback_data=f'calendar/day/{date[0]}-{date[1]}-{date[2]}'
                )
            ]
        ])

        return keyboard_markup

    except KeyError:
        keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
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

        return keyboard_markup


def reply_return_edit_description_keyboard() -> InlineKeyboardMarkup:
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data=f'calendar/day/add_task/edit_description/'
            )
        ]
    ])

    return keyboard_markup


def reply_edit_description_keyboard(date: str, data: dict) -> InlineKeyboardMarkup:
    date = date.split('-')

    try:
        if data['time']:
            pass

        keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
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
        return keyboard_markup

    except KeyError:
        keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
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

        return keyboard_markup


def reply_edit_time_keyboard() -> InlineKeyboardMarkup:

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
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

    return keyboard_markup


def reply_check_task_keyboard(date: str) -> InlineKeyboardMarkup:
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Сохранить', callback_data=f'calendar/day/add_task/save')
        ],
        [
            InlineKeyboardButton(text='Изменить', callback_data=f'calendar/day/add_task/edit_title/{date}')
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data=f'calendar/date/{date}')
        ],
    ])

    return keyboard_markup


def reply_list_task_keyboard(date: str, list_tasks: list, parameter: str, page: int = 1) -> InlineKeyboardMarkup:
    tasks_per_page = 5
    start_index = (page - 1) * tasks_per_page
    end_index = start_index + tasks_per_page
    current_tasks = list_tasks[start_index:end_index]

    keyboard_buttons = []

    # Генерация кнопок для текущей страницы задач
    for task in current_tasks:
        start_time = task.start_datetime.strftime("%H:%M")
        end_time = task.end_datetime.strftime("%H:%M")
        task_button = InlineKeyboardButton(
            text=f'{start_time}-{end_time} {task.title}',
            callback_data=f'calendar/day/{parameter}/{task.id}'
        )
        keyboard_buttons.append([task_button])

    # Кнопки навигации по страницам
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(text='<-', callback_data=f'calendar/day/list_{parameter}/{date}/{page - 1}'))
    if end_index < len(list_tasks):
        navigation_buttons.append(
            InlineKeyboardButton(text='->', callback_data=f'calendar/day/list_{parameter}/{date}/{page + 1}'))

    if navigation_buttons:
        keyboard_buttons.append(navigation_buttons)

    # Кнопка "Назад"
    keyboard_buttons.append([
        InlineKeyboardButton(text='Назад', callback_data=f'calendar/day/{date}')
    ])

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard_markup


def enter_to_delete(date: str, task_id: int) -> InlineKeyboardMarkup:

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data=f'calendar/day/enter_del_task/{task_id}')
        ],
        [
            InlineKeyboardButton(text='Нет', callback_data=f'calendar/day/{date}')
        ]
    ])

    return keyboard_markup


def enter_to_successful_task(task_id: int) -> InlineKeyboardMarkup:
    task_id = str(task_id)

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data=f'successful_task/True/{task_id}')
        ],
        [
            InlineKeyboardButton(text='Нет', callback_data=f'successful_task/False/{task_id}')
        ]
    ])

    return keyboard_markup
