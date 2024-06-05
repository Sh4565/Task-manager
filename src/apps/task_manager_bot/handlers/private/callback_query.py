
import logging

from datetime import date
from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from apps.task_manager_bot.states import CreateTask
from apps.task_manager_bot.language import get_language
from apps.task_manager_bot.keyboards import callback_data
from apps.task_manager_bot.db import task_methods, user_methods
from apps.task_manager_bot.utils import message_edit_text_keyboard


callback_query_router = Router()
logger = logging.getLogger(__name__)


@callback_query_router.callback_query(F.data == "start_menu")
async def start_menu(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    text = get_language('start_menu', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$FIRST_NAME', callback.from_user.first_name),
        reply_markup=callback_data.reply_start_keyboard(language_user)
    )


@callback_query_router.callback_query(F.data == "calendar")
async def calendar(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()
    year = date.today().year
    mouth = date.today().month

    str_mouth = str(mouth)
    if len(str_mouth) != 2:
        str_mouth = f'0{mouth}'

    text = get_language('calendar', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$DATE', f'{year}-{str_mouth}'),
        reply_markup=callback_data.reply_calendar_keyboard(language_user)
    )


@callback_query_router.callback_query(F.data.startswith("calendar/next"))
async def calendar_next(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()
    data = callback.data.split('/')[2].split('-')
    year = int(data[0])
    mouth = int(data[1]) + 1

    if mouth == 13:
        year += 1
        mouth = 1

    str_mouth = str(mouth)
    if len(str_mouth) != 2:
        str_mouth = f'0{mouth}'

    text = get_language('calendar', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$DATE', f'{year}-{str_mouth}'),
        reply_markup=callback_data.reply_calendar_keyboard(language_user, year, mouth)
    )


@callback_query_router.callback_query(F.data.startswith("calendar/back"))
async def calendar_back(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()
    data = callback.data.split('/')[2].split('-')
    year = int(data[0])
    mouth = int(data[1]) - 1

    if mouth == 0:
        year -= 1
        mouth = 12

    str_mouth = str(mouth)
    if len(str_mouth) != 2:
        str_mouth = f'0{mouth}'

    text = get_language('calendar', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$DATE', f'{year}-{str_mouth}'),
        reply_markup=callback_data.reply_calendar_keyboard(language_user, year, mouth)
    )


@callback_query_router.callback_query(F.data.startswith("calendar/date"))
async def calendar_date(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()
    data = callback.data.split('/')[2].split('-')
    year = int(data[0])
    mouth = int(data[1])

    str_mouth = str(mouth)
    if len(str_mouth) != 2:
        str_mouth = f'0{mouth}'

    text = get_language('calendar', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$DATE', f'{year}-{str_mouth}'),
        reply_markup=callback_data.reply_calendar_keyboard(language_user, year, mouth)
    )


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/title"))
async def calendar_create_title(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    date_calendar = callback.data.split('/')[4]
    await state.update_data(date=date_calendar)

    text = get_language('calendar_create_title', language_user)
    await callback.message.answer(
        text=text,
        reply_markup=callback_data.reply_tasks_day_keyboard(date_calendar, language_user)
    )
    await state.set_state(CreateTask.title)


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/edit_title"))
async def calendar_day_edit_title(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    date_calendar = callback.data.split('/')[4]
    data = await state.get_data()
    await state.update_data(date=date_calendar)

    text = get_language('calendar_day_edit_title', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$TITLE', data['title']),
        reply_markup=callback_data.reply_edit_title_keyboard(date_calendar, data, language_user)
    )
    await state.set_state(CreateTask.title)


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/description"))
async def create_description_task(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    data = await state.get_data()

    text = get_language('create_description_task', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_return_add_task_keyboard(data['date'], language_user)
    )
    await state.set_state(CreateTask.description)


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/edit_description"))
async def calendar_day_edit(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    data = await state.get_data()

    text = get_language('create_title_task_1', language_user)
    text = text.replace('$DESCRIPTION', data['description'])
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_edit_description_keyboard(data['date'], data, language_user)
    )
    await state.set_state(CreateTask.description)


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/time"))
async def create_title_task(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:

    text = get_language('create_description_task_2', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_return_edit_description_keyboard(language_user)
    )
    await state.set_state(CreateTask.time)


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/edit_time"))
async def edit_time(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    data = await state.get_data()
    text = get_language('create_description_task_1', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$TIME', data['time']),
        reply_markup=callback_data.reply_edit_time_keyboard(language_user)
    )
    await state.set_state(CreateTask.time)


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/task"))
async def check_task(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    data = await state.get_data()

    text = get_language('check_task_save', language_user)
    text = text.replace('$TIME', data['time']).replace('$TITLE', data['title'])
    text = text.replace('$DESCRIPTION', data['description'])
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_check_task_keyboard(data['date'], language_user)
    )


@callback_query_router.callback_query(F.data.startswith("calendar/day/add_task/save"))
async def save_task(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    data = await state.get_data()

    user_id = callback.from_user.id
    try:
        task_id = data['task_id']
    except KeyError:
        task_id = 0

    user = await user_methods.get_user(callback.from_user.id)

    await task_methods.add_task(
        user_id=user_id,
        date=data['date'],
        title=data['title'],
        time=data['time'],
        timezone=user.timezone,
        description=data['description'],
        task_id=task_id
    )
    tasks = await task_methods.get_tasks(user, data['date'])

    schedule = ''
    for task in tasks:
        start_datetime = task.start_datetime.strftime("%H:%M")
        end_datetime = task.end_datetime.strftime("%H:%M")
        schedule += f'{start_datetime}-{end_datetime} {task.title}\n{task.description}\n\n'

    text = get_language('list_task', language_user)
    text = text.replace('$SCHEDULER', schedule).replace('$DATE', data['date'])
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_check_day_keyboard(data['date'], language_user)
    )
    await state.clear()


@callback_query_router.callback_query(F.data.startswith("calendar/day/list_edit"))
async def list_task_edit(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    date = callback.data.split('/')[3]
    page = int(callback.data.split('/')[4])
    user = await user_methods.get_user(callback.from_user.id)
    tasks = await task_methods.get_tasks(user, date)

    text = get_language('list_task_edit', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_list_task_keyboard(language_user, date, tasks, 'edit_task', page)
    )


@callback_query_router.callback_query(F.data.startswith("calendar/day/list_del_task"))
async def list_task_del(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    date = callback.data.split('/')[3]
    page = int(callback.data.split('/')[4])
    user = await user_methods.get_user(callback.from_user.id)
    tasks = await task_methods.get_tasks(user, date)

    text = get_language('list_task_del', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_list_task_keyboard(language_user, date, tasks, 'del_task', page)
    )


@callback_query_router.callback_query(F.data.startswith("calendar/day/del_task"))
async def del_task(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    try:
        task_id = int(callback.data.split('/')[3])
        user = await user_methods.get_user(callback.from_user.id)
        task = await task_methods.get_task(task_id, user)

        text = get_language('del_task', language_user)
        text = text.replace('$START_TIME', task.start_datetime.strftime("%H:%M"))
        text = text.replace('$END_TIME', task.end_datetime.strftime("%H:%M"))
        text = text.replace('$TITLE', task.title)
        await message_edit_text_keyboard(
            obj=callback,
            text=text,
            reply_markup=callback_data.enter_to_delete(task.date.strftime("%Y-%m-%d"), task_id, language_user)
        )

    except TypeError:
        pass


@callback_query_router.callback_query(F.data.startswith("calendar/day/enter_del_task/"))
async def enter_del_task(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    task_id = int(callback.data.split('/')[3])

    user_id = callback.from_user.id
    user = await user_methods.get_user(callback.from_user.id)
    task = await task_methods.get_task(task_id, user)
    date_schedule = task.date.strftime("%Y-%m-%d")
    await task_methods.del_task(task_id, user_id)

    text = get_language('enter_del_task', language_user)
    await callback.answer(text)
    tasks = await task_methods.get_tasks(user, date_schedule)

    schedule = ''
    for task in tasks:
        start_datetime = task.start_datetime.strftime("%H:%M")
        end_datetime = task.end_datetime.strftime("%H:%M")
        schedule += f'{start_datetime}-{end_datetime} {task.title}\n{task.description}\n\n'

    text = get_language('list_task', language_user)
    text = text.replace('$SCHEDULER', schedule).replace('$DATE', date_schedule)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_check_day_keyboard(date_schedule, language_user)
    )
    # except TypeError:
    #     pass


@callback_query_router.callback_query(F.data.startswith("calendar/day/edit_task/"))
async def task_edit(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    task_id = int(callback.data.split('/')[3])
    user = await user_methods.get_user(callback.from_user.id)
    task = await task_methods.get_task(task_id, user)
    await state.update_data(task_id=task.id)
    await state.update_data(title=task.title)
    await state.update_data(date=task.date.strftime("%Y-%m-%d"))
    await state.update_data(description=task.description)
    await state.update_data(time=f'{task.start_datetime.strftime("%H:%M")}-{task.end_datetime.strftime("%H:%M")}')

    data = await state.get_data()
    text = get_language('calendar_day_edit_title', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text.replace('$TITLE', data['title']),
        reply_markup=callback_data.reply_edit_title_keyboard(task.date.strftime("%Y-%m-%d"), data, language_user)
    )
    await state.set_state(CreateTask.title)


@callback_query_router.callback_query(F.data.startswith("calendar/day"))
async def calendar_day(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    date_schedule = callback.data.split('/')[2]
    user = await user_methods.get_user(callback.from_user.id)
    tasks = await task_methods.get_tasks(user, date_schedule)

    schedule = ''
    for task in tasks:
        start_datetime = task.start_datetime.strftime("%H:%M")
        end_datetime = task.end_datetime.strftime("%H:%M")
        schedule += f'{start_datetime}-{end_datetime} {task.title}\n{task.description}\n\n'

    text = get_language('list_task', language_user)
    text = text.replace('$SCHEDULER', schedule).replace('$DATE', date_schedule)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_check_day_keyboard(date_schedule, language_user)
    )


@callback_query_router.callback_query(F.data.startswith("successful_task/True"))
async def task_completed(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    task_id = int(callback.data.split('/')[2])
    user = await user_methods.get_user(callback.from_user.id)
    task = await task_methods.get_task(task_id, user)

    await task_methods.add_task(
        user_id=callback.from_user.id,
        date=task.date,
        title=task.title,
        time=f'{task.start_datetime.strftime("%H:%M")}-{task.end_datetime.strftime("%H:%M")}',
        timezone=user.timezone,
        description=task.description,
        task_id=task_id,
        done=True
    )

    text = get_language('task_completed', language_user)
    await callback.message.edit_text(text=text)


@callback_query_router.callback_query(F.data.startswith("successful_task/False"))
async def task_completed(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    task_id = int(callback.data.split('/')[2])
    user = await user_methods.get_user(callback.from_user.id)
    task = await task_methods.get_task(task_id, user)

    await task_methods.add_task(
        user_id=callback.from_user.id,
        date=task.date,
        title=task.title,
        time=f'{task.start_datetime.strftime("%H:%M")}-{task.end_datetime.strftime("%H:%M")}',
        timezone=user.timezone,
        description=task.description,
        task_id=task_id,
        done=False
    )

    text = get_language('task_completed_bad', language_user)
    await callback.message.edit_text(text=text)


@callback_query_router.callback_query(F.data.startswith("profile"))
async def profile(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    user = await user_methods.get_user(callback.from_user.id)
    done_task, not_done, none_done, all_tasks = await task_methods.get_statistic(callback.from_user.id)
    if user.timezone:
        timezone = user.timezone
    else:
        timezone = 'UTC'

    text = get_language('profile', language_user)
    text = text.replace('$DONE_TASK', str(done_task)).replace('$NOT_DONE', str(not_done))
    text = text.replace('$NONE_DONE', str(none_done)).replace('$ALL_TASK', str(all_tasks))
    text = text.replace('$TIMEZONE', timezone).replace('$LANGUAGE', user.language)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.profile_keyboard(language_user)
    )


@callback_query_router.callback_query(F.data.startswith("set_list_timezones"))
async def set_list_timezones(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    page = int(callback.data.split('/')[1])

    text = get_language('set_list_timezones', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.reply_list_timezone_keyboard(language_user, page)
    )


@callback_query_router.callback_query(F.data.startswith("set_timezone"))
async def set_timezone(callback: CallbackQuery, state: FSMContext, bot: Bot, language_user: str) -> None:
    await state.clear()
    timezone = callback.data.split('/')[1].replace('-', '/')

    await user_methods.update_user(callback.from_user, timezone=timezone)
    text = get_language('set_timezone', language_user)
    text = text.replace('$TIMEZONE', timezone)
    await callback.answer(text)
    await bot.answer_callback_query(callback.id)
    await profile(callback, state, language_user)


@callback_query_router.callback_query(F.data.startswith("choice_language"))
async def choice_language(callback: CallbackQuery, state: FSMContext, language_user: str) -> None:
    await state.clear()

    text = get_language('choice_language', language_user)
    await message_edit_text_keyboard(
        obj=callback,
        text=text,
        reply_markup=callback_data.language_keyboard(language_user)
    )


@callback_query_router.callback_query(F.data.startswith("set_language"))
async def set_language(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    language = callback.data.split('/')[1]

    await user_methods.update_user(callback.from_user, language=language)
    await profile(callback, state, language)
