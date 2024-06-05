
import logging

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters.command import Command

from apps.task_manager_bot.db import user_methods
from apps.task_manager_bot.language import get_language
from apps.task_manager_bot.keyboards import callback_data


commands_router = Router()
logger = logging.getLogger(__name__)


@commands_router.message(Command('start'))
async def echo_handler(message: Message, bot: Bot, language_user: str) -> None:
    user = await user_methods.get_user(message.from_user.id)

    if not user.timezone:
        text = get_language('not_timezone', language_user)
        await bot.send_message(
                chat_id=message.from_user.id,
                text=text
            )

    text = get_language('start_menu', language_user)
    await message.answer(
        text=text.replace('$FIRST_NAME', message.from_user.first_name),
        reply_markup=callback_data.reply_start_keyboard(language_user)
    )


@commands_router.message(Command('set_timezone'))
async def echo_handler(message: Message, language_user: str) -> None:
    timezone = message.text.split(' ')[1]

    await user_methods.update_user(message.from_user, timezone=timezone)

    text = get_language('set_timezone', language_user)
    await message.answer(text=text.replace('$TIMEZONE', timezone))
