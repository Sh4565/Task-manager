
from pytz import utc
from django.conf import settings
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler


dp = Dispatcher()
bot = Bot(token=settings.TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

scheduler = AsyncIOScheduler(timezone=utc)

