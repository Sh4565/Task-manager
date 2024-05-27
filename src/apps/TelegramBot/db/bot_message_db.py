
import logging
from pprint import pprint

from aiogram.types import Message
from asgiref.sync import sync_to_async

from apps.TelegramBot.models import TelegramMessage


logger = logging.getLogger(__name__)


@sync_to_async
def add_message(message: Message):
    telegram_message = TelegramMessage.objects.create(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
        message_id=message.message_id,
        text=message.text,
        date=message.date
    )

    date = f'{message.chat.id} {message.from_user.id} {message.message_id} {message.text} {message.date}'
    logger.debug(f'Сообщение успешно зарегистрированно в БД {date}')
