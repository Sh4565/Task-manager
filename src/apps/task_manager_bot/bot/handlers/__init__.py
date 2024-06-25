
from aiogram import Dispatcher

from .private import private_routers


def init_routers(dp: Dispatcher) -> None:
    dp.include_routers(
        private_routers,
    )

