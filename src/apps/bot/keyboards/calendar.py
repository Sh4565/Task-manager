
import calendar

from datetime import datetime
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup


def calendar_button():

    calendar_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Пн', callback_data=f'weekly_calendar/day/1'),
            InlineKeyboardButton(text='Вт', callback_data=f'weekly_calendar/day/2'),
            InlineKeyboardButton(text='Ср', callback_data=f'weekly_calendar/day/3'),
            InlineKeyboardButton(text='Чт', callback_data=f'weekly_calendar/day/4'),
            InlineKeyboardButton(text='Пт', callback_data=f'weekly_calendar/day/5'),
            InlineKeyboardButton(text='Сб', callback_data=f'weekly_calendar/day/6'),
            InlineKeyboardButton(text='Вс', callback_data=f'weekly_calendar/day/7')
        ],
        [
            InlineKeyboardButton(text='Пн', callback_data=f'weekly_calendar/day/1'),
            InlineKeyboardButton(text='Вт', callback_data=f'weekly_calendar/day/2'),
            InlineKeyboardButton(text='Ср', callback_data=f'weekly_calendar/day/3'),
            InlineKeyboardButton(text='Чт', callback_data=f'weekly_calendar/day/4'),
            InlineKeyboardButton(text='Пт', callback_data=f'weekly_calendar/day/5'),
            InlineKeyboardButton(text='Сб', callback_data=f'weekly_calendar/day/6'),
            InlineKeyboardButton(text='Вс', callback_data=f'weekly_calendar/day/7')
        ],
        [
            InlineKeyboardButton(text='Пн', callback_data=f'weekly_calendar/day/1'),
            InlineKeyboardButton(text='Вт', callback_data=f'weekly_calendar/day/2'),
            InlineKeyboardButton(text='Ср', callback_data=f'weekly_calendar/day/3'),
            InlineKeyboardButton(text='Чт', callback_data=f'weekly_calendar/day/4'),
            InlineKeyboardButton(text='Пт', callback_data=f'weekly_calendar/day/5'),
            InlineKeyboardButton(text='Сб', callback_data=f'weekly_calendar/day/6'),
            InlineKeyboardButton(text='Вс', callback_data=f'weekly_calendar/day/7')
        ],
        [
            InlineKeyboardButton(text='Пн', callback_data=f'weekly_calendar/day/1'),
            InlineKeyboardButton(text='Вт', callback_data=f'weekly_calendar/day/2'),
            InlineKeyboardButton(text='Ср', callback_data=f'weekly_calendar/day/3'),
            InlineKeyboardButton(text='Чт', callback_data=f'weekly_calendar/day/4'),
            InlineKeyboardButton(text='Пт', callback_data=f'weekly_calendar/day/5'),
            InlineKeyboardButton(text='Сб', callback_data=f'weekly_calendar/day/6'),
            InlineKeyboardButton(text='Вс', callback_data=f'weekly_calendar/day/7')
        ],
        [
            InlineKeyboardButton(text='Пн', callback_data=f'weekly_calendar/day/1'),
            InlineKeyboardButton(text='Вт', callback_data=f'weekly_calendar/day/2'),
            InlineKeyboardButton(text='Ср', callback_data=f'weekly_calendar/day/3'),
            InlineKeyboardButton(text='Чт', callback_data=f'weekly_calendar/day/4'),
            InlineKeyboardButton(text='Пт', callback_data=f'weekly_calendar/day/5'),
            InlineKeyboardButton(text='Сб', callback_data=f'weekly_calendar/day/6'),
            InlineKeyboardButton(text='Вс', callback_data=f'weekly_calendar/day/7')
        ],
        [
            InlineKeyboardButton(text='<-', callback_data=f'weekly_calendar/back'),
            InlineKeyboardButton(text='->', callback_data=f'weekly_calendar/next')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='main_menu')
        ]
    ])

    return calendar_buttons
