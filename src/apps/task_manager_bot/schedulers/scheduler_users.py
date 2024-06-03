
import logging

from aiogram import Bot

from apps.task_manager_bot.keyboards import callback_data
from apps.task_manager_bot.main import bot, scheduler
from apps.task_manager_bot.db.task_methods import get_all_tasks, get_task


logger = logging.getLogger(__name__)


async def start_task(bot: Bot, task_id: int, user_id: int) -> None:
    task = await get_task(task_id, user_id)
    await bot.send_message(
        chat_id=user_id,
        text=f'Время приступать к выполнению задания "{task.title}"!'
    )


async def end_task(bot: Bot, task_id: int, user_id: int) -> None:
    task = await get_task(task_id, user_id)
    await bot.send_message(
        chat_id=user_id,
        text=f'Вы выполнили задание "{task.title}"?',
        reply_markup=callback_data.enter_to_successful_task(task.id)
    )


async def add_users_scheduler():
    tasks = await get_all_tasks()

    for task in tasks:
        try:
            start_time = f'{task.date.strftime("%Y-%m-%d")} {task.start_datetime.strftime("%H:%M:%S")}'
            end_time = f'{task.date.strftime("%Y-%m-%d")} {task.end_datetime.strftime("%H:%M:%S")}'
            scheduler.add_job(start_task, 'date', run_date=start_time, args=[bot, task.id, task.user_id], id=f'{str(task.id)}start')
            scheduler.add_job(end_task, 'date', run_date=end_time, args=[bot, task.id, task.user_id], id=f'{str(task.id)}end')
            logger.debug(f'Задача {task.id} успешно запланирована')

        except Exception as err:
            logger.error(f'Задача {task.id} не была добавлена в планировщик {err}')


def init_scheduler():
    logger.debug('Проверяю наличие новых задач пользователей')
    scheduler.add_job(add_users_scheduler, 'interval', minutes=1)

    scheduler.start()