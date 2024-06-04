
import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

from apps.task_manager_bot.db import user_methods


logger = logging.getLogger(__name__)


class UserUpdateMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        user = data['event_from_user']

        if await user_methods.get_user(user.id):
            await user_methods.update_user(user)

        else:
            await user_methods.create_user(user)

        # До обработчика
        result = await handler(event, data)
        # После обработчика
        return result
