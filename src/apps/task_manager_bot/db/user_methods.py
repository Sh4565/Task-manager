
import logging
import datetime
import django.db.utils

from asgiref.sync import sync_to_async
from aiogram.types import Message, User
from django.db import close_old_connections
from django.core.exceptions import ObjectDoesNotExist

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
        logger.debug(f'Повідомлення користувача [{message.from_user.id}] успішно зареєстровано')

    try:
        return main()
    except django.db.utils.OperationalError:
        logger.error("OperationalError: З'єднання з базою даних втрачено. Спроба відновити з'єднання...")
        close_old_connections()
        return main()

    except Exception as err:
        logger.error(f'Повідомлення користувача [{message.from_user.id}] не було зареєстровано. Помилка: {err}')


@sync_to_async
def create_user(user: User):
    def main() -> None:
        TelegramUser.objects.create(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            timezone=None,
            language=user.language_code,
            last_activity=datetime.datetime.now(datetime.timezone.utc)
        )

    try:
        main()
    except django.db.utils.OperationalError:
        logger.error("OperationalError: З'єднання з базою даних втрачено. Спроба відновити з'єднання...")
        close_old_connections()
        main()

    except Exception as err:
        logger.error(f'Не вдалося зареєструвати користувача [{user.id}]. Помилка: {err}')


@sync_to_async
def update_user(user: User, timezone: str = None, language: str = None):
    def main() -> None:
        user_update = TelegramUser.objects.get(user_id=user.id)

        if timezone:
            user_update.timezone = timezone
        elif language:
            user_update.language = language

        user_update.first_name = user.first_name
        user_update.last_name = user.last_name
        user_update.username = user.username
        user_update.last_activity = datetime.datetime.now(datetime.timezone.utc)

        user_update.save()

    try:
        main()
    except django.db.utils.OperationalError:
        logger.error("OperationalError: З'єднання з базою даних втрачено. Спроба відновити з'єднання...")
        close_old_connections()
        main()

    except Exception as err:
        logger.error(f'Не вдалося оновити користувача [{user.id}]. Помилка: {err}')


@sync_to_async
def get_user(user_id: int) -> TelegramUser | None:
    def main() -> TelegramUser:
        return TelegramUser.objects.get(user_id=user_id)

    try:
        return main()

    except django.db.utils.OperationalError:
        logger.error("OperationalError: З'єднання з базою даних втрачено. Спроба відновити з'єднання...")
        close_old_connections()
        return main()

    except ObjectDoesNotExist:
        return None

    except Exception as err:
        logger.error(f'Неможливо отримати користувача [{user_id}]. Помилка: {err}')
