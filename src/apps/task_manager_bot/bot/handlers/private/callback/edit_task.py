
import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from apps.task_manager_bot.bot.states import CreateTask
from apps.task_manager_bot.utils.language import get_language
from apps.task_manager_bot.bot.keyboards import callback_data
from apps.task_manager_bot.db import task_methods, user_methods
from apps.task_manager_bot.utils import message_edit_text_keyboard


edit_task_router = Router()
logger = logging.getLogger(__name__)


@edit_task_router.callback_query(F.data.startswith("calendar/day/list_edit"))
async def list_task_edit(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    date = callback.data.split('/')[3]
    page = int(callback.data.split('/')[4])
    user = await user_methods.get_user(callback.from_user.id)
    tasks = await task_methods.get_tasks(user, date)

    text = get_language('list_task_edit', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_list_task_keyboard(language_user, date, tasks, 'edit_task', page)
    )


@edit_task_router.callback_query(F.data.startswith("calendar/day/edit_task/"))
async def task_edit(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    task_id = int(callback.data.split('/')[3])
    user = await user_methods.get_user(callback.from_user.id)
    task = await task_methods.get_task(task_id, user)
    await state.update_data(task_id=task.id)
    await state.update_data(title=task.title)
    await state.update_data(date=task.date.strftime("%Y-%m-%d"))
    await state.update_data(description=task.description)
    await state.update_data(
        time=f'{task.start_datetime.strftime("%H:%M")}-{task.end_datetime.strftime("%H:%M")}'
    )

    data = await state.get_data()
    text = get_language('calendar_day_edit_title', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$TITLE', data['title']),
        reply_markup=callback_data.reply_edit_title_keyboard(task.date.strftime("%Y-%m-%d"),
                                                             data, language_user)
    )
    await state.set_state(CreateTask.title)
