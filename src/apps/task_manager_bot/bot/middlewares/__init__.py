
from aiogram import Dispatcher

from .get_language import LanguageMiddleware
from .log_message import LogMessageMiddleware
from .user_update import UserUpdateMiddleware
from .log_callback import LogCallbackMiddleware


def setup_middleware(dp: Dispatcher):
    dp.callback_query.middleware(LogCallbackMiddleware())
    dp.message.middleware(LogMessageMiddleware())
    dp.update.outer_middleware(UserUpdateMiddleware())
    dp.update.outer_middleware(LanguageMiddleware())
