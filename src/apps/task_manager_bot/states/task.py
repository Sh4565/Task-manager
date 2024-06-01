
from aiogram.fsm.state import StatesGroup, State


class CreateTask(StatesGroup):
    task_id = State()
    date = State()
    title = State()
    description = State()
    time = State()
