
from aiogram import Dispatcher

from .message import MessageMiddleware
from .userupdate import UserUpdateMiddleware


def setup_middleware(dp: Dispatcher):
    dp.update.middleware(MessageMiddleware())
    dp.update.outer_middleware(UserUpdateMiddleware())
