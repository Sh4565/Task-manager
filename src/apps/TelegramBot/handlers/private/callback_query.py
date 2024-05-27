
import time
import logging

from datetime import date
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from apps.TelegramBot.fsm import CreateTask
from apps.TelegramBot.db.get_task import get_task
from apps.TelegramBot.db.add_task import add_task
from apps.TelegramBot.utils import message_edit_text_keyboard
from apps.TelegramBot.keyboards import callback_data


callback_query_router = Router()
logger = logging.getLogger(__name__)


@callback_query_router.callback_query(F.data == "start_menu")
async def start_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await message_edit_text_keyboard(
        obj=callback,
        text=f'Привет {callback.from_user.first_name}! Выбери действие',
        reply_markup=callback_data.reply_start_keyboard()
    )


@callback_query_router.callback_query(F.data == "calendar")
async def calendar(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    year = date.today().year
    mouth = date.today().month

    str_mouth = str(mouth)
    if len(str_mouth) != 2:
        str_mouth = f'0{mouth}'

    await message_edit_text_keyboard(
        obj=callback,
        text=f'Выбери день для редактирования\n{year}-{str_mouth}',
        reply_markup=callback_data.reply_calendar_keyboard()
    )


@callback_query_router.callback_query(F.data.startswith("calendar/next"))
async def calendar_next(callback: CallbackQuery, state: FSMContext) -> None:
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

    await message_edit_text_keyboard(
        obj=callback,
        text=f'Выбери день для редактирования\n{year}-{str_mouth}',
        reply_markup=callback_data.reply_calendar_keyboard(year, mouth)
    )


@callback_query_router.callback_query(F.data.startswith("calendar/back"))
async def calendar_back(callback: CallbackQuery, state: FSMContext) -> None:
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

    await message_edit_text_keyboard(
        obj=callback,
        text=f'Выбери день для редактирования\n{year}-{str_mouth}',
        reply_markup=callback_data.reply_calendar_keyboard(year, mouth)
    )


@callback_query_router.callback_query(F.data.startswith("calendar/date"))
async def calendar_date(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    data = callback.data.split('/')[2].split('-')
    year = int(data[0])
    mouth = int(data[1])

    str_mouth = str(mouth)
    if len(str_mouth) != 2:
        str_mouth = f'0{mouth}'

    logger.debug(callback.data)
    await message_edit_text_keyboard(
        obj=callback,
        text=f'Выбери день для редактирования\n{year}-{str_mouth}',
        reply_markup=callback_data.reply_calendar_keyboard(year, mouth)
    )


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/title"))
async def calendar_day_edit(callback: CallbackQuery, state: FSMContext) -> None:
    date_calendar = callback.data.split('/')[4]
    await state.update_data(date=date_calendar)
    await message_edit_text_keyboard(
        obj=callback,
        text='Введите название задачи',
        reply_markup=callback_data.reply_return_calendar_keyboard(date_calendar)
    )
    await state.set_state(CreateTask.title)


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/edit_title"))
async def calendar_day_edit(callback: CallbackQuery, state: FSMContext) -> None:
    date_calendar = callback.data.split('/')[4]
    data = await state.get_data()
    await state.update_data(date=date_calendar)
    await message_edit_text_keyboard(
        obj=callback,
        text=f"Введите новое название или нажмите кнопку далее чтобы оставить \"{data['title']}\"",
        reply_markup=callback_data.reply_edit_title_keyboard(date_calendar, data)
    )
    await state.set_state(CreateTask.title)


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/description"))
async def create_title_task(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await message_edit_text_keyboard(
        obj=callback,
        text='Теперь введите описание своей задачи',
        reply_markup=callback_data.reply_return_add_task_keyboard(data['date'])
    )
    await state.set_state(CreateTask.description)


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/edit_description"))
async def calendar_day_edit(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await message_edit_text_keyboard(
        obj=callback,
        text=f"Введите новое описание или нажмите кнопку далее чтобы оставить \"{data['description']}\"",
        reply_markup=callback_data.reply_edit_description_keyboard(data['date'], data)
    )
    await state.set_state(CreateTask.description)


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/time"))
async def create_title_task(callback: CallbackQuery, state: FSMContext) -> None:
    await message_edit_text_keyboard(
        obj=callback,
        text='Введите промежуток времени отведенное на выполнение задания. \nПример: 09:00-11:30',
        reply_markup=callback_data.reply_return_edit_description_keyboard()
    )
    await state.set_state(CreateTask.time)


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/edit_time"))
async def edit_time(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    logger.debug(f"{data['date']} {data['title']} {data['description']}")
    await message_edit_text_keyboard(
        obj=callback,
        text=f"Введите новый промежуток времени или нажмите кнопку далее чтобы оставить \"{data['time']}\"",
        reply_markup=callback_data.reply_edit_time_keyboard()
    )
    await state.set_state(CreateTask.time)


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/task"))
async def check_task(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await message_edit_text_keyboard(
        obj=callback,
        text=f'{data["time"]} {data["title"]}\n{data["description"]}\n\nСохранить?',
        reply_markup=callback_data.reply_check_task_keyboard(data['date'])
    )


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/save"))
async def save_task(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()

    user_id = callback.from_user.id
    await add_task(user_id=user_id, date=data['date'], title=data['title'], time=data['time'], description=data['description'])
    tasks = await get_task(user_id, data['date'])

    schedule = ''
    for task in tasks:
        schedule += f'{task.start_datetime}-{task.end_datetime} {task.title}\n{task.description}\n\n'
    await message_edit_text_keyboard(
        obj=callback,
        text=f"{schedule}{data['date']}\nВыберите действие",
        reply_markup=callback_data.reply_check_day_keyboard(data['date'])
    )
    await state.clear()


@callback_query_router.callback_query(F.data.startswith("calendar/day"))
async def calendar_day(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    user_id = callback.from_user.id
    date_schedule = callback.data.split('/')[2]
    tasks = await get_task(user_id, date_schedule)

    schedule = ''
    for task in tasks:
        schedule += f'{task.start_datetime}-{task.end_datetime} {task.title}\n{task.description}\n\n'
    await message_edit_text_keyboard(
        obj=callback,
        text=f'{schedule}{date_schedule}\nВыберите действие',
        reply_markup=callback_data.reply_check_day_keyboard(date_schedule)
    )
