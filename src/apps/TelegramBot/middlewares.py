
import logging

from pprint import pprint
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from apps.TelegramBot.db.bot_message_db import add_message
from apps.TelegramBot.db.bot_user_db import update_of_create_tg_user


logger = logging.getLogger(__name__)


class CustomMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user = data['event_from_user']

        create_status = await update_of_create_tg_user(user)
        self.counter += 1
        data['counter'] = self.counter
        return await handler(event, data)


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
            await add_message(event.message)
        elif isinstance(event.callback_query, CallbackQuery):
            logger.debug(event.callback_query.data)

        self.counter += 1
        data['counter'] = self.counter
        return await handler(event, data)
