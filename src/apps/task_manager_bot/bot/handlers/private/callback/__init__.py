
from aiogram import Router

from .menus import menus_router
from .del_task import del_task_router
from .calendar import calendar_router
from .edit_task import edit_task_router
from .dialog_task import dialog_task_router
from .notifications import notifications_router
from .settings_user import settings_user_router


callback_routes = Router()
callback_routes.include_routers(
    dialog_task_router,
    calendar_router,
    edit_task_router,
    del_task_router,
    notifications_router,
    settings_user_router,
    menus_router,
)
