
import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

from apps.task_manager_bot.db import user_methods


logger = logging.getLogger(__name__)


class LanguageMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        user = data['event_from_user']
        from_user = await user_methods.get_user(user.id)
        if from_user:
            language_user: str = from_user.language
            data['language_user'] = language_user
        else:
            data['language_user'] = 'en'

        result = await handler(event, data)
        return result
