
import logging

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

from apps.task_manager_bot.db import user_methods


logger = logging.getLogger(__name__)


class UserUpdateMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user = data['event_from_user']

        await user_methods.update_of_create_tg_user(user)
        self.counter += 1
        data['counter'] = self.counter
        return await handler(event, data)
