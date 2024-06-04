
import logging
import datetime

import django.db.utils
import pytz

from asgiref.sync import sync_to_async
from django.db import close_old_connections

from apps.task_manager_bot.models import Task, TelegramUser


logger = logging.getLogger(__name__)


@sync_to_async
def get_all_tasks() -> list:

    def main() -> list:
        good_task = []

        current_time = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M")
        current_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

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
def add_task(user_id: int, date: str, time: str, timezone: str, title: str, description: str, task_id: int = 0, done=None) -> None:
    def main() -> None:

        start_time = datetime.datetime.strptime(f'{date} {time.split("-")[0]}', "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(f'{date} {time.split("-")[1]}', "%Y-%m-%d %H:%M")

        local_tz = pytz.timezone(timezone)
        start_time = local_tz.localize(start_time)
        end_time = local_tz.localize(end_time)

        start_time_utc = start_time.astimezone(pytz.utc)
        end_time_utc = end_time.astimezone(pytz.utc)

        if task_id == 0:
            Task.objects.create(
                user_id=user_id,
                date=date,
                start_datetime=start_time_utc.strftime("%H:%M"),
                end_datetime=end_time_utc.strftime("%H:%M"),
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
def get_tasks(user: TelegramUser, date: str) -> list:
    def main() -> list:
        logger.debug(type(user.user_id))
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        tasks = list(Task.objects.filter(user_id=user.user_id, date=date_obj))

        for task in tasks:
            start_time_utc = datetime.datetime.strptime(f'{task.date} {task.start_datetime}', "%Y-%m-%d %H:%M:%S")
            end_time_utc = datetime.datetime.strptime(f'{task.date} {task.end_datetime}', "%Y-%m-%d %H:%M:%S")

            local_tz = pytz.utc
            start_time_utc = local_tz.localize(start_time_utc)
            end_time_utc = local_tz.localize(end_time_utc)

            start_time = start_time_utc.astimezone(pytz.timezone(user.timezone))
            end_time = end_time_utc.astimezone(pytz.timezone(user.timezone))

            task.start_datetime = start_time
            task.end_datetime = end_time

            tasks[tasks.index(task)] = task

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
def get_task(task_id: int, user: TelegramUser) -> Task:
    def main() -> Task:

        task = Task.objects.get(id=task_id, user_id=user.user_id)

        start_time_utc = datetime.datetime.strptime(f'{task.date} {task.start_datetime}', "%Y-%m-%d %H:%M:%S")
        end_time_utc = datetime.datetime.strptime(f'{task.date} {task.end_datetime}', "%Y-%m-%d %H:%M:%S")

        local_tz = pytz.utc
        start_time_utc = local_tz.localize(start_time_utc)
        end_time_utc = local_tz.localize(end_time_utc)

        start_time = start_time_utc.astimezone(pytz.timezone(user.timezone))
        end_time = end_time_utc.astimezone(pytz.timezone(user.timezone))

        task.start_datetime = start_time
        task.end_datetime = end_time

        return task

    try:
        return main()
    except django.db.utils.OperationalError:
        logger.error('OperationalError: Соединение с базой данных потеряно. Попытка восстановить соединение...')
        close_old_connections()
        return main()


@sync_to_async
def get_statistic(user_id: int) -> tuple[int, int, int, int]:
    def main():
        done_task = len(Task.objects.filter(user_id=user_id, done=True))
        not_done = len(Task.objects.filter(user_id=user_id, done=False))
        none_done = len(Task.objects.filter(user_id=user_id, done=None))
        all_tasks = len(Task.objects.filter(user_id=user_id))

        return done_task, not_done, none_done, all_tasks

    try:
        return main()
    except django.db.utils.OperationalError:
        logger.error('OperationalError: Соединение с базой данных потеряно. Попытка восстановить соединение...')
        close_old_connections()
        return main()
