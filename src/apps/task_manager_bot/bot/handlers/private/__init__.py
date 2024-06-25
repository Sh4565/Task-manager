
from aiogram import Router

from .message import messages_routers
from .commands import commands_routers
from .callback import callback_routes


private_routers = Router()
private_routers.include_routers(
    messages_routers,
    commands_routers,
    callback_routes,
)
