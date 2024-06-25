
import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from apps.task_manager_bot.utils.language import get_language
from apps.task_manager_bot.bot.keyboards import callback_data
from apps.task_manager_bot.db import task_methods, user_methods
from apps.task_manager_bot.utils import message_edit_text_keyboard


del_task_router = Router()
logger = logging.getLogger(__name__)


@del_task_router.callback_query(F.data.startswith("calendar/day/list_del_task"))
async def list_task_del(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    date = callback.data.split('/')[3]
    page = int(callback.data.split('/')[4])
    user = await user_methods.get_user(callback.from_user.id)
    tasks = await task_methods.get_tasks(user, date)

    text = get_language('list_task_del', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_list_task_keyboard(language_user, date, tasks, 'del_task', page)
    )


@del_task_router.callback_query(F.data.startswith("calendar/day/del_task"))
async def del_task(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    try:
        task_id = int(callback.data.split('/')[3])
        user = await user_methods.get_user(callback.from_user.id)
        task = await task_methods.get_task(task_id, user)

        text = get_language('del_task', language_user)
        text = text.replace('$START_TIME', task.start_datetime.strftime("%H:%M"))
        text = text.replace('$END_TIME', task.end_datetime.strftime("%H:%M"))
        text = text.replace('$TITLE', task.title)
        await message_edit_text_keyboard(
            obj=callback,
            text=text,
            reply_markup=callback_data.enter_to_delete(task.date.strftime("%Y-%m-%d"), task_id, language_user)
        )

    except TypeError:
        pass


@del_task_router.callback_query(F.data.startswith("calendar/day/enter_del_task/"))
async def enter_del_task(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    task_id = int(callback.data.split('/')[3])

    user_id = callback.from_user.id
    user = await user_methods.get_user(callback.from_user.id)
    task = await task_methods.get_task(task_id, user)
    date_schedule = task.date.strftime("%Y-%m-%d")
    await task_methods.del_task(task_id, user_id)

    text = get_language('enter_del_task', language_user)
    await callback.answer(text)
    tasks = await task_methods.get_tasks(user, date_schedule)

    schedule = ''
    for task in tasks:
        start_datetime = task.start_datetime.strftime("%H:%M")
        end_datetime = task.end_datetime.strftime("%H:%M")
        schedule += f'{start_datetime}-{end_datetime} {task.title}\n{task.description}\n\n'

    text = get_language('list_task', language_user)
    text = text.replace('$SCHEDULER', schedule).replace('$DATE', date_schedule)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_check_day_keyboard(date_schedule, language_user)
    )
