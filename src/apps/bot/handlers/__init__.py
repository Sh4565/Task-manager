
from aiogram import Dispatcher

from .private import init_private_routers


def init_routers(dp: Dispatcher) -> None:
    init_private_routers(dp)
