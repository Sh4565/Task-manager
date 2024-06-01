
from django.conf import settings
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


dp = Dispatcher()
bot = Bot(token=settings.TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
