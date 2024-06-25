
from aiogram import Router

from .dialog_task_create import dialog_task_router


messages_routers = Router()
messages_routers.include_routers(
    dialog_task_router,
)
