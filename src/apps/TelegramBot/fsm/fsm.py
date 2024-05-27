
from aiogram.fsm.state import StatesGroup, State


class CreateTask(StatesGroup):
    date = State()
    title = State()
    description = State()
    time = State()
