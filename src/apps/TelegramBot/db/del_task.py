
import logging

from asgiref.sync import sync_to_async

from apps.TelegramBot.models import Task


logger = logging.getLogger(__name__)


@sync_to_async
def del_task(task_id: int, user_id: int):
    try:
        Task.objects.get(id=task_id, user_id=user_id).delete()
        logger.debug(f'Пользователь[{user_id}] успешно удалил задачу')
    except Exception as err:
        logger.error(f'Пользователь[{user_id}] не смог удалить задачу: {err}')
