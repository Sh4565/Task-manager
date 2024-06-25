
import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from apps.task_manager_bot.utils.language import get_language
from apps.task_manager_bot.bot.keyboards import callback_data
from apps.task_manager_bot.db import task_methods, user_methods
from apps.task_manager_bot.utils import message_edit_text_keyboard


menus_router = Router()
logger = logging.getLogger(__name__)


@menus_router.callback_query(F.data == "start_menu")
async def start_menu(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    text = get_language('start_menu', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$FIRST_NAME', callback.from_user.first_name),
        reply_markup=callback_data.reply_start_keyboard(language_user)
    )


@menus_router.callback_query(F.data.startswith("profile"))
async def profile(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    user = await user_methods.get_user(callback.from_user.id)
    done_task, not_done, none_done, all_tasks = await task_methods.get_statistic(callback.from_user.id)
    if user.timezone:
        timezone = user.timezone
    else:
        timezone = 'UTC'

    text = get_language('profile', language_user)
    text = text.replace('$DONE_TASK', str(done_task)).replace('$NOT_DONE', str(not_done))
    text = text.replace('$NONE_DONE', str(none_done)).replace('$ALL_TASK', str(all_tasks))
    text = text.replace('$TIMEZONE', timezone).replace('$LANGUAGE', user.language)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.profile_keyboard(language_user)
    )


@menus_router.callback_query(F.data.startswith("calendar/day"))
async def calendar_day(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    date_schedule = callback.data.split('/')[2]
    user = await user_methods.get_user(callback.from_user.id)
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
