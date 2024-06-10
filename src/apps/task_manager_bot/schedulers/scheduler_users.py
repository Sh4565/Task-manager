
import logging

from aiogram import Bot
from apscheduler.jobstores.base import ConflictingIdError

from apps.task_manager_bot.utils.language import get_language
from apps.task_manager_bot.main import bot, scheduler
from apps.task_manager_bot.keyboards import callback_data
from apps.task_manager_bot.db import task_methods, user_methods


logger = logging.getLogger(__name__)


async def start_task(bot: Bot, task_id: int, user_id: int) -> None:
    user = await user_methods.get_user(user_id)
    task = await task_methods.get_task(task_id, user)

    text = get_language('scheduler_start_task', user.language)
    await bot.send_message(
        chat_id=user_id,
        text=text.replace('$TASK_TITLE', task.title)
    )


async def end_task(bot: Bot, task_id: int, user_id: int) -> None:
    user = await user_methods.get_user(user_id)
    task = await task_methods.get_task(task_id, user)

    text = get_language('scheduler_end_task', user.language)
    await bot.send_message(
        chat_id=user_id,
        text=text.replace('$TASK_TITLE', task.title),
        reply_markup=callback_data.enter_to_successful_task(task.id, user.language)
    )


async def add_users_scheduler():
    logger.debug('Перевіряю наявність нових завдань користувачів')
    tasks = await task_methods.get_all_tasks()

    for task in tasks:
        try:
            start_time = f'{task.date.strftime("%Y-%m-%d")} {task.start_datetime.strftime("%H:%M:%S")}'
            end_time = f'{task.date.strftime("%Y-%m-%d")} {task.end_datetime.strftime("%H:%M:%S")}'
            scheduler.add_job(
                start_task,
                'date',
                run_date=start_time,
                args=[bot, task.id, task.user_id],
                id=f'{str(task.id)}start'
            )
            scheduler.add_job(
                end_task,
                'date',
                run_date=end_time,
                args=[bot, task.id, task.user_id],
                id=f'{str(task.id)}end'
            )
            logger.debug(f'Завдання {task.id} успішно заплановане')

        except ConflictingIdError:
            pass

    logger.debug('Закінчив перевірку наявності нових завдань користувачів')
