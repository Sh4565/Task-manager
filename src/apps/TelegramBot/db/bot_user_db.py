
import logging

from aiogram.types import User
from asgiref.sync import sync_to_async

from apps.TelegramBot.models import TelegramUser


logger = logging.getLogger(__name__)


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
