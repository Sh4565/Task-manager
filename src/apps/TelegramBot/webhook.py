
import logging

from aiogram import Bot, Dispatcher
from django.conf import settings

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{settings.WEBHOOK_URL}{settings.WEBHOOK_PATH}")


async def on_shutdown(dp: Dispatcher, bot: Bot):
    await bot.delete_webhook()
    await dp.storage.close()
