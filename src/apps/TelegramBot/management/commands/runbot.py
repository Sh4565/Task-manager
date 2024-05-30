
import asyncio
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.TelegramBot import dp, bot
from apps.TelegramBot.handlers import init_routers
from apps.TelegramBot.middlewares import setup_middleware


logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


async def run_polling():
    setup_middleware(dp)
    init_routers(dp)

    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'Telegram TelegramBot'

    def handle(self, *args, **options):
        try:
            asyncio.run(run_polling())
        except Exception as err:
            logger.error(f'Ошибка: {err}')
