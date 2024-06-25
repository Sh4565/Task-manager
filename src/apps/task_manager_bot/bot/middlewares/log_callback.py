
import logging

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from typing import Callable, Dict, Any, Awaitable

from apps.task_manager_bot.db import user_methods


logger = logging.getLogger(__name__)


class LogCallbackMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        callback: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:

        logger.debug(callback.data)

        result = await handler(callback, data)
        return result

