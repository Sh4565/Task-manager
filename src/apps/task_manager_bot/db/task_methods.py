
import logging
import django.db.utils

from datetime import datetime
from asgiref.sync import sync_to_async
from django.db import close_old_connections

from apps.task_manager_bot.models import Task


logger = logging.getLogger(__name__)


@sync_to_async
def get_all_tasks() -> list:

    def main() -> list:
        good_task = []

        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().strftime("%Y-%m-%d")

        tasks = Task.objects.all()

        for task in tasks:
            if current_date <= task.date.strftime("%Y-%m-%d") and current_time <= task.start_datetime.strftime("%H:%M"):
                good_task.append(task)

        return good_task

    try:
        return main()
    except django.db.utils.OperationalError:
        logger.error('OperationalError: Соединение с базой данных потеряно. Попытка восстановить соединение...')
        close_old_connections()
        return main()


@sync_to_async
def get_tasks(user_id: int, date: str) -> list:
    def main() -> list:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        tasks = list(Task.objects.filter(user_id=user_id, date=date_obj))

        for i in range(len(tasks) - 1):
            for j in range(len(tasks) - i - 1):
                start_time1 = tasks[j].start_datetime.strftime("%H:%M")
                start_time2 = tasks[j + 1].start_datetime.strftime("%H:%M")
                if start_time1 > start_time2:
                    tasks[j], tasks[j + 1] = tasks[j + 1], tasks[j]

        return tasks

    try:
        return main()
    except django.db.utils.OperationalError:
        logger.error('OperationalError: Соединение с базой данных потеряно. Попытка восстановить соединение...')
        close_old_connections()
        return main()


@sync_to_async
def add_task(user_id: int, date: str, time: str, title: str, description: str, task_id: int = 0, done=None) -> None:
    def main() -> None:
        if task_id == 0:
            Task.objects.create(
                user_id=user_id,
                date=date,
                start_datetime=time.split('-')[0],
                end_datetime=time.split('-')[1],
                title=title,
                description=description,
                done=done
            )

        else:
            task = Task.objects.get(id=task_id)
            task.user_id = user_id
            task.date = date
            task.start_datetime = time.split('-')[0]
            task.end_datetime = time.split('-')[1]
            task.title = title
            task.description = description
            task.done = done
            task.save()

    try:
        main()
    except django.db.utils.OperationalError:
        logger.error('OperationalError: Соединение с базой данных потеряно. Попытка восстановить соединение...')
        close_old_connections()
        main()


@sync_to_async
def del_task(task_id: int, user_id: int):
    def main() -> None:
        Task.objects.get(id=task_id, user_id=user_id).delete()

    try:
        main()
    except django.db.utils.OperationalError:
        logger.error('OperationalError: Соединение с базой данных потеряно. Попытка восстановить соединение...')
        close_old_connections()
        main()


@sync_to_async
def get_task(task_id: int, user_id: int) -> Task:
    def main() -> Task:
        return Task.objects.get(id=task_id, user_id=user_id)

    try:
        return main()
    except django.db.utils.OperationalError:
        logger.error('OperationalError: Соединение с базой данных потеряно. Попытка восстановить соединение...')
        close_old_connections()
        return main()
