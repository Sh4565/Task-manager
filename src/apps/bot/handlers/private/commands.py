
import logging

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters.command import Command

from apps.bot.keyboards.callback_data import reply_start_keyboard


commands_router = Router()
logger = logging.getLogger(__name__)


@commands_router.message(Command('start'))
async def echo_handler(message: Message, bot: Bot) -> None:
    await message.answer(
        text=f'Привет {message.from_user.first_name}! Выбери действие',
        reply_markup=reply_start_keyboard()
    )
