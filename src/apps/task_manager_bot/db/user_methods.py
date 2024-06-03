
import logging
import datetime
import django.db.utils

from asgiref.sync import sync_to_async
from aiogram.types import Message, User
from django.db import close_old_connections

from apps.task_manager_bot.models import TelegramMessage, TelegramUser


logger = logging.getLogger(__name__)


@sync_to_async
def add_message(message: Message) -> None:
    def main() -> None:
        TelegramMessage.objects.create(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            message_id=message.message_id,
            text=message.text,
            date=message.date
        )
        logger.debug(f'Сообщение пользователя [{message.from_user.id}] успешно зарегистрировано')

    try:
        return main()
    except django.db.utils.OperationalError:
        logger.error('OperationalError: Соединение с базой данных потеряно. Попытка восстановить соединение...')
        close_old_connections()
        return main()

    except Exception as err:
        logger.error(f'Сообщение пользователя [{message.from_user.id}] не было зарегистрировано. Ошибка: {err}')


@sync_to_async
def update_of_create_tg_user(user: User):
    def main() -> None:
        language = user.language_code

        if user.language_code not in ['en', 'ua', 'ru']:
            language = 'en'

        defaults_dict = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'utc': None,
            'language': language,
            'last_activity': datetime.datetime.now(datetime.timezone.utc)
        }
        telegram_user, create_status = TelegramUser.objects.update_or_create(user_id=user.id, defaults=defaults_dict)

        if create_status is False:
            logger.debug(f'Успешно обновлен user в БД [{user.id}] {user.first_name}')
        else:
            logger.debug(f'Успешно создан user в БД [{user.id}] {user.first_name}')

    try:
        return main()
    except django.db.utils.OperationalError:
        logger.error('OperationalError: Соединение с базой данных потеряно. Попытка восстановить соединение...')
        close_old_connections()
        return main()

    except Exception as err:
        logger.error(f'Данные пользователя [{user.id}] не удалось зарегистрировать. Ошибка: {err}')


@sync_to_async
def get_user(user_id: int) -> TelegramUser:
    def main() -> TelegramUser:
        return TelegramUser.objects.get(user_id=user_id)

    try:
        return main()
    except django.db.utils.OperationalError:
        logger.error('OperationalError: Соединение с базой данных потеряно. Попытка восстановить соединение...')
        close_old_connections()
        return main()

    except Exception as err:
        logger.error(f'Не удалось получить пользователя [{message.from_user.id}]. Ошибка: {err}')