
import logging

from asgiref.sync import sync_to_async
from aiogram.types import Message, User

from apps.TelegramBot.models import TelegramMessage, TelegramUser


logger = logging.getLogger(__name__)


@sync_to_async
def add_message(message: Message):
    TelegramMessage.objects.create(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
        message_id=message.message_id,
        text=message.text,
        date=message.date
    )

    date = f'{message.chat.id} {message.from_user.id} {message.message_id} {message.text} {message.date}'
    logger.debug(f'Сообщение успешно зарегистрировано в БД {date}')


@sync_to_async
def update_of_create_tg_user(data: User):
    defaults_dict = {
        'first_name': data.first_name,
        'last_name': data.last_name,
        'username': data.username,
    }
    telegram_user, create_status = TelegramUser.objects.update_or_create(user_id=data.id, defaults=defaults_dict)

    if create_status is False:
        logger.debug(f'Успешно обновлен user в БД {data.first_name} {data.last_name} {data.username}')
    else:
        logger.debug(f'Успешно создан user в БД {data.first_name} {data.last_name} {data.username}')

    return create_status
