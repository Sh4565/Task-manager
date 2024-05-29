
import logging

from asgiref.sync import sync_to_async

from apps.TelegramBot.models import Task


logger = logging.getLogger(__name__)


@sync_to_async
def add_task(user_id: int, date: str, time: str, title: str, description: str, task_id: int = 0):
    try:
        if task_id == 0:
            task = Task.objects.create(
                user_id=user_id,
                date=date,
                start_datetime=time.split('-')[0],
                end_datetime=time.split('-')[1],
                title=title,
                description=description,
                done=None
            )
            logger.debug(f'Пользователь[{user_id}] успешно создал задачу')

        else:
            task = Task.objects.get(id=task_id)
            task.user_id = user_id
            task.date = date
            task.start_datetime = time.split('-')[0]
            task.end_datetime = time.split('-')[1]
            task.title = title
            task.description = description
            task.done = None
            task.save()
            logger.debug(f'Пользователь[{user_id}] успешно обновил задачу')

    except Exception as err:
        logger.error(f'Пользователь[{user_id}] не смог создать задачу: {err}')
