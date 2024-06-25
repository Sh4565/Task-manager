
from aiogram import Router

from .main_commands import main_commands_router


commands_routers = Router()
commands_routers.include_routers(
    main_commands_router,
)
