
from aiogram.filters import Filter
from aiogram.types import Message


class PrivateFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.type == 'private':
            return True
        else:
            return False
