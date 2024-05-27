
import logging

from aiogram.types import Message
from asgiref.sync import sync_to_async

from apps.TelegramBot.models import Task


logger = logging.getLogger(__name__)


@sync_to_async
def add_task(user_id: int, date: str, time: str, title: str, description: str):
    try:
        Task.objects.create(
            user_id=user_id,
            date=date,
            start_datetime=time.split('-')[0],
            end_datetime=time.split('-')[1],
            title=title,
            description=description,
            done=None
        )

        logger.debug(f'Пользователь[{user_id}] успешно создал задачу')
    except Exception as err:
        logger.error(f'Пользователь[{user_id}] не смог создать задачу: {err}')
