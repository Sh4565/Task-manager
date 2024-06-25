
import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from apps.task_manager_bot.utils.language import get_language
from apps.task_manager_bot.db import task_methods, user_methods


notifications_router = Router()
logger = logging.getLogger(__name__)


@notifications_router.callback_query(F.data.startswith("successful_task"))
async def task_completed(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    completed = callback.data.split('/')[1]
    if completed == 'False':
        completed = False
    elif completed == 'True':
        completed = True

    task_id = int(callback.data.split('/')[2])
    user = await user_methods.get_user(callback.from_user.id)
    task = await task_methods.get_task(task_id, user)

    await task_methods.add_task(
        user_id=callback.from_user.id,
        date=task.date,
        title=task.title,
        time=f'{task.start_datetime.strftime("%H:%M")}-{task.end_datetime.strftime("%H:%M")}',
        timezone=user.timezone,
        description=task.description,
        task_id=task_id,
        done=completed
    )

    if completed:
        text = get_language('task_completed', language_user)
        await callback.message.edit_text(text=text)
    else:
        text = get_language('task_completed_bad', language_user)
        await callback.message.edit_text(text=text)
