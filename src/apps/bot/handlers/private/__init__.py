
from aiogram import Dispatcher

from .other import other_router
from .commands import commands_router
from .callback_query import callback_query_router


def init_private_routers(dp: Dispatcher) -> None:
    dp.include_routers(
        commands_router,
        callback_query_router,
        other_router,
    )
