
import time
import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from apps.task_manager_bot.states import CreateTask
from apps.task_manager_bot.language import get_language
from apps.task_manager_bot.keyboards import callback_data


message_router = Router()
logger = logging.getLogger(__name__)


@message_router.message(CreateTask.title)
async def create_title_task(message: Message, state: FSMContext, language_user: str) -> None:
    await state.update_data(title=message.text)
    data = await state.get_data()

    try:
        text = get_language('create_title_task_1', language_user)
        if data['description']:
            await message.answer(
                text=text.replace('$DESCRIPTION', data['description']),
                reply_markup=callback_data.reply_edit_description_keyboard(data['date'], data, language_user)
            )

    except KeyError:
        text = get_language('create_title_task_2', language_user)
        await message.answer(
            text=text,
            reply_markup=callback_data.reply_return_add_task_keyboard(data['date'], language_user)
        )

    logger.debug(f'Додано назву {message.text}')
    await state.set_state(CreateTask.description)


@message_router.message(CreateTask.description)
async def create_description_task(message: Message, state: FSMContext, language_user: str) -> None:
    await state.update_data(description=message.text)

    data = await state.get_data()

    try:
        if data['time']:
            text = get_language('create_description_task_1', language_user)
            await message.answer(
                text=text.replace('$TIME', data['time']),
                reply_markup=callback_data.reply_edit_time_keyboard(language_user)
            )

    except KeyError:
        text = get_language('create_description_task_2', language_user)
        await message.answer(
            text=text,
            reply_markup=callback_data.reply_return_edit_description_keyboard(language_user)
        )
    logger.debug(f'Додано опис {message.text}')
    await state.set_state(CreateTask.time)


@message_router.message(CreateTask.time)
async def create_description_task(message: Message, state: FSMContext, language_user: str) -> None:
    try:
        start_time = message.text.split('-')[0]
        end_time = message.text.split('-')[1]

        try:
            valid_start_time = time.strptime(start_time, '%H:%M')
            valid_end_time = time.strptime(end_time, '%H:%M')
            if valid_start_time < valid_end_time:
                await state.update_data(time=message.text)
                data = await state.get_data()

                print(data)

                text = get_language('check_task_save', language_user)
                text = text.replace('$TIME', data['time']).replace('$TITLE', data['title'])
                text = text.replace('$DESCRIPTION', data['description'])
                await message.answer(
                    text=text,
                    reply_markup=callback_data.reply_check_task_keyboard(data['date'], language_user)
                )
                logger.debug(f'Додано час {message.text}')
            else:
                text = get_language('create_description_task_error', language_user)
                await message.answer(
                    text=text,
                    reply_markup=callback_data.reply_return_edit_description_keyboard(language_user)
                )

        except ValueError:
            text = get_language('create_description_task_error', language_user)
            await message.answer(
                text=text,
                reply_markup=callback_data.reply_return_edit_description_keyboard(language_user)
            )

    except IndexError:
        text = get_language('create_description_task_error', language_user)
        await message.answer(
            text=text,
            reply_markup=callback_data.reply_return_edit_description_keyboard(language_user)
        )
