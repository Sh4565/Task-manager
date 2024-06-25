
from aiogram import Dispatcher

from .commands import commands_router
from .callback_query import callback_query_router
from .message import message_router


def init_private_routers(dp: Dispatcher) -> None:
    dp.include_routers(
        message_router,
        commands_router,
        callback_query_router,
    )
