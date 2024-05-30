
import logging

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from apps.TelegramBot.db import user_methods


logger = logging.getLogger(__name__)


class MessageMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        if isinstance(event.message, Message):
            await user_methods.add_message(event.message)
        elif isinstance(event.callback_query, CallbackQuery):
            logger.debug(event.callback_query.data)

        self.counter += 1
        data['counter'] = self.counter
        return await handler(event, data)
