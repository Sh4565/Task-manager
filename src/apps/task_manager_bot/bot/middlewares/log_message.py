
import logging

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from apps.task_manager_bot.db import user_methods


logger = logging.getLogger(__name__)


class LogMessageMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: Dict[str, Any]
    ) -> Any:

        await user_methods.add_message(message)

        result = await handler(message, data)
        return result

