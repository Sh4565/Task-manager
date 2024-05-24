
import asyncio
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.bot import dp, bot
from apps.bot.middlewares import CustomMiddleware, MessageMiddleware
from apps.bot.handlers import init_routers


logger = logging.getLogger('run_bot')
logger.setLevel(settings.LOG_LEVEL)


async def run_polling():
    dp.update.outer_middleware(CustomMiddleware())
    dp.update.middleware(MessageMiddleware())
    init_routers(dp)

    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'Telegram bot'

    def handle(self, *args, **options):
        try:
            asyncio.run(run_polling())
        except Exception as err:
            logger.error(f'Ошибка: {err}')
