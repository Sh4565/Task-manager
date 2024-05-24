
from aiogram import Router, Bot
from aiogram.types import Message

from apps.bot.keyboards.calendar import calendar_button

other_router = Router()


@other_router.message()
async def echo_handler(message: Message, bot: Bot) -> None:
    await message.answer(
        text='?!',
        reply_markup=calendar_button()
    )
