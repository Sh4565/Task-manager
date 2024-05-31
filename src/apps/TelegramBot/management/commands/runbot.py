
import asyncio
import logging

from aiohttp import web
from django.conf import settings
from django.core.management.base import BaseCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from apps.TelegramBot import dp, bot
from apps.TelegramBot.handlers import init_routers
from apps.TelegramBot.middlewares import setup_middleware
from apps.TelegramBot.webhook import on_startup, on_shutdown


logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


async def run_polling():
    setup_middleware(dp)
    init_routers(dp)

    await dp.start_polling(bot)


def run_webhook():
    setup_middleware(dp)
    init_routers(dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )

    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=settings.WEB_SERVER_HOST, port=settings.WEB_SERVER_PORT)


class Command(BaseCommand):
    help = 'Telegram TelegramBot'

    def add_arguments(self, parser):
        parser.add_argument("launch", type=str, help='Способ запуска телеграм бота')

    def handle(self, *args, **options):
        try:
            if options['launch'] == 'poling' or options['launch'] == '':
                asyncio.run(run_polling())
            if options['launch'] == 'webhook':
                run_webhook()

        except Exception as err:
            logger.error(f'Ошибка: {err}')
