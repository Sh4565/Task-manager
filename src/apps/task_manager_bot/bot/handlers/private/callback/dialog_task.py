
import logging

from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from apps.task_manager_bot.bot.states import CreateTask
from apps.task_manager_bot.utils.language import get_language
from apps.task_manager_bot.bot.keyboards import callback_data
from apps.task_manager_bot.db import task_methods, user_methods
from apps.task_manager_bot.utils import message_edit_text_keyboard


dialog_task_router = Router()
logger = logging.getLogger(__name__)


@dialog_task_router.callback_query(F.data.startswith("calendar/day/add_task/title"))
async def calendar_create_title(callback: CallbackQuery, bot: Bot, state: FSMContext,
                                language_user: str) -> None:

    user = await user_methods.get_user(callback.from_user.id)
    if not user.timezone:
        text = get_language('not_timezone', language_user)
        await bot.send_message(
                chat_id=callback.from_user.id,
                text=text
            )
    else:
        date_calendar = callback.data.split('/')[4]
        await state.update_data(date=date_calendar)

        text = get_language('calendar_create_title', language_user)
        await callback.message.answer(
            text=text,
            reply_markup=callback_data.reply_tasks_day_keyboard(date_calendar, language_user)
        )
        await state.set_state(CreateTask.title)


@dialog_task_router.callback_query(F.data.startswith("calendar/day/add_task/edit_title"))
async def edit_title(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    date_calendar = callback.data.split('/')[4]
    data = await state.get_data()
    await state.update_data(date=date_calendar)

    text = get_language('calendar_day_edit_title', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$TITLE', data['title']),
        reply_markup=callback_data.reply_edit_title_keyboard(date_calendar, data, language_user)
    )
    await state.set_state(CreateTask.title)


@dialog_task_router.callback_query(F.data.startswith("calendar/day/add_task/description"))
async def create_description_task(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    data = await state.get_data()

    text = get_language('create_description_task', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_return_add_task_keyboard(data['date'], language_user)
    )
    await state.set_state(CreateTask.description)


@dialog_task_router.callback_query(F.data.startswith("calendar/day/add_task/edit_description"))
async def edit_description(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    data = await state.get_data()

    text = get_language('create_title_task_1', language_user)
    text = text.replace('$DESCRIPTION', data['description'])
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_edit_description_keyboard(data['date'], data, language_user)
    )
    await state.set_state(CreateTask.description)


@dialog_task_router.callback_query(F.data.startswith("calendar/day/add_task/time"))
async def create_title_task(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:

    text = get_language('create_description_task_2', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_return_edit_description_keyboard(language_user)
    )
    await state.set_state(CreateTask.time)


@dialog_task_router.callback_query(F.data.startswith("calendar/day/add_task/edit_time"))
async def edit_time(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    data = await state.get_data()
    text = get_language('create_description_task_1', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$TIME', data['time']),
        reply_markup=callback_data.reply_edit_time_keyboard(language_user)
    )
    await state.set_state(CreateTask.time)


@dialog_task_router.callback_query(F.data.startswith("calendar/day/add_task/task"))
async def check_task(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    data = await state.get_data()

    text = get_language('check_task_save', language_user)
    text = text.replace('$TIME', data['time']).replace('$TITLE', data['title'])
    text = text.replace('$DESCRIPTION', data['description'])
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_check_task_keyboard(data['date'], language_user)
    )


@dialog_task_router.callback_query(F.data.startswith("calendar/day/add_task/save"))
async def save_task(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    data = await state.get_data()

    user_id = callback.from_user.id
    try:
        task_id = data['task_id']
    except KeyError:
        task_id = 0

    user = await user_methods.get_user(callback.from_user.id)

    await task_methods.add_task(
        user_id=user_id,
        date=data['date'],
        title=data['title'],
        time=data['time'],
        timezone=user.timezone,
        description=data['description'],
        task_id=task_id
    )
    tasks = await task_methods.get_tasks(user, data['date'])

    schedule = ''
    for task in tasks:
        start_datetime = task.start_datetime.strftime("%H:%M")
        end_datetime = task.end_datetime.strftime("%H:%M")
        schedule += f'{start_datetime}-{end_datetime} {task.title}\n{task.description}\n\n'

    text = get_language('list_task', language_user)
    text = text.replace('$SCHEDULER', schedule).replace('$DATE', data['date'])
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_check_day_keyboard(data['date'], language_user)
    )
    await state.clear()
