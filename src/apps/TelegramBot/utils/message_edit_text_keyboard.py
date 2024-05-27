
from typing import Union
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup


async def message_edit_text_keyboard(obj: Union[Message, CallbackQuery], text: str, reply_markup: InlineKeyboardMarkup):
    if isinstance(obj, Message):
        message = obj
        await message.edit_text(text=text)
        await message.edit_reply_markup(reply_markup=reply_markup)
    elif isinstance(obj, CallbackQuery):
        callback = obj
        await callback.message.edit_text(text=text)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)
