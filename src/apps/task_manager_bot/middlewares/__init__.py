
from aiogram import Dispatcher

from .log_message import LogMessageMiddleware
from .user_update import UserUpdateMiddleware


def setup_middleware(dp: Dispatcher):
    dp.message.middleware(LogMessageMiddleware())
    dp.update.outer_middleware(UserUpdateMiddleware())
