
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

    if not user.timezone:
        await bot.send_message(
                chat_id=message.from_user.id,
                text='Пожалуйста настройте свой часовой пояс. Вы можете это сделать перейдя "Профиль->Сменить часовой пояс" или же прописать команду, например `/set_timezone Europe/Kiev`'
            )

    await message.answer(
        text=f'Привет {message.from_user.first_name}! Выбери действие',
        reply_markup=callback_data.reply_start_keyboard()
    )


@commands_router.message(Command('set_timezone'))
async def echo_handler(message: Message, bot: Bot) -> None:
    timezone = message.text.split(' ')[1]

    await user_methods.update_user(message.from_user, timezone=timezone)

    await message.answer(text=f'Установлен часовой пояс: {timezone}')
