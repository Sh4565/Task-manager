
import time
import logging

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from apps.TelegramBot.fsm import CreateTask
from apps.TelegramBot.keyboards import callback_data
from apps.TelegramBot.utils import message_edit_text_keyboard


message_router = Router()
logger = logging.getLogger(__name__)


@message_router.message(CreateTask.title)
async def create_title_task(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    data = await state.get_data()

    try:
        if data['description']:
            await message.answer(
                text=f"Введите новое описание или нажмите кнопку далее чтобы оставить \"{data['description']}\"",
                reply_markup=callback_data.reply_edit_description_keyboard(data['date'], data)
            )

    except KeyError:
        await message.answer(
            text='Теперь введите описание своей задачи',
            reply_markup=callback_data.reply_return_add_task_keyboard(data['date'])
        )
    logger.debug(f'Добавленно название {message.text}')
    await state.set_state(CreateTask.description)


@message_router.message(CreateTask.description)
async def create_description_task(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)

    data = await state.get_data()

    try:
        if data['time']:
            await message.answer(
                text=f"Введите новый промежуток времени или нажмите кнопку далее чтобы оставить \"{data['time']}\"",
                reply_markup=callback_data.reply_edit_time_keyboard()
            )

    except KeyError:
        await message.answer(
            text='Введите промежуток времени отведенное на выполнение задания. \nПример: 09:00-11:30',
            reply_markup=callback_data.reply_return_edit_description_keyboard()
        )
    logger.debug(f'Добавленно описание {message.text}')
    await state.set_state(CreateTask.time)


@message_router.message(CreateTask.time)
async def create_description_task(message: Message, state: FSMContext) -> None:
    try:
        start_time = message.text.split('-')[0]
        end_time = message.text.split('-')[1]

        try:
            valid_start_time = time.strptime(start_time, '%H:%M')
            valid_end_time = time.strptime(end_time, '%H:%M')
            if valid_start_time < valid_end_time:
                await state.update_data(time=message.text)
                data = await state.get_data()
                await message.answer(
                    text=f'{data["time"]} {data["title"]}\n{data["description"]}\n\nСохранить?',
                    reply_markup=callback_data.reply_check_task_keyboard(data['date'])
                )
                logger.debug(f'Добавленно время {message.text}')
            else:
                logger.error(
                    f'Пользователь[{message.from_user.id}] при попытке создать или отредактировать задание ввел время "{message.text}"')
                await message.answer(
                    text='Вы допустили ошибку при вводе времени. Пожалуйста придерживайтесь примера: 09:00-11:30',
                    reply_markup=callback_data.reply_return_edit_description_keyboard()
                )

        except ValueError:
            logger.error(
                f'Пользователь {message.from_user.id} при попытке создать или отредактировать задание ввел время "{message.text}"')
            await message.answer(
                text='Вы допустили ошибку при вводе времени. Пожалуйста придерживайтесь примера: 09:00-11:30',
                reply_markup=callback_data.reply_return_edit_description_keyboard()
            )

    except IndexError:
        logger.error(
            f'Пользователь {message.from_user.id} при попытке создать или отредактировать задание ввел время "{message.text}"')
        await message.answer(
            text='Вы допустили ошибку при вводе времени. Пожалуйста придерживайтесь примера: 09:00-11:30',
            reply_markup=callback_data.reply_return_edit_description_keyboard()
        )
