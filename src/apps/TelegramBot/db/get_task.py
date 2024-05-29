
import logging

from datetime import datetime
from asgiref.sync import sync_to_async

from apps.TelegramBot.models import Task


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
def get_task(task_id: int, user_id: int):
    return Task.objects.get(id=task_id, user_id=user_id)
