
import logging

from datetime import datetime
from pprint import pprint
from aiogram.types import Message
from asgiref.sync import sync_to_async

from apps.TelegramBot.models import Task


logger = logging.getLogger(__name__)


@sync_to_async
def get_task(user_id: int, date: str):
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    tasks = Task.objects.filter(user_id=user_id, date=date_obj)
    return list(tasks)
