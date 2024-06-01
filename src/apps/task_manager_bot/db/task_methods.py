
import logging

from datetime import datetime
from asgiref.sync import sync_to_async

from apps.task_manager_bot.models import Task


logger = logging.getLogger(__name__)


@sync_to_async
def get_tasks(user_id: int, date: str) -> list:
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    tasks = list(Task.objects.filter(user_id=user_id, date=date_obj))

    for i in range(len(tasks) - 1):
        for j in range(len(tasks) - i - 1):
            start_time1 = tasks[j].start_datetime.strftime("%H:%M")
            start_time2 = tasks[j + 1].start_datetime.strftime("%H:%M")
            if start_time1 > start_time2:
                tasks[j], tasks[j + 1] = tasks[j + 1], tasks[j]

    return tasks


@sync_to_async
def add_task(user_id: int, date: str, time: str, title: str, description: str, task_id: int = 0):
    try:
        if task_id == 0:
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


@sync_to_async
def del_task(task_id: int, user_id: int):
    try:
        Task.objects.get(id=task_id, user_id=user_id).delete()
        logger.debug(f'Пользователь[{user_id}] успешно удалил задачу')
    except Exception as err:
        logger.error(f'Пользователь[{user_id}] не смог удалить задачу: {err}')


@sync_to_async
def get_task(task_id: int, user_id: int):
    return Task.objects.get(id=task_id, user_id=user_id)
