
import logging

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters.command import Command

from apps.task_manager_bot.keyboards import callback_data
from apps.task_manager_bot.db import user_methods


commands_router = Router()
logger = logging.getLogger(__name__)


@commands_router.message(Command('start'))
async def echo_handler(message: Message, bot: Bot) -> None:
    user = await user_methods.get_user(message.from_user.id)

    # if user.utc and user.language:
    await message.answer(
        text=f'Привет {message.from_user.first_name}! Выбери действие',
        reply_markup=callback_data.reply_start_keyboard()
    )
