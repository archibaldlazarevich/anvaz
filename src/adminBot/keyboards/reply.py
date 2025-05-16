from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.database.func.data_func import (
    get_all_non_employee,
    get_all_dir,
    get_all_emp,
    get_all_jobs,
    get_all_dell,
)


async def check_staff():
    """
    Функция для составления клавиатуры со всем персоналом
    :return:
    """
    all_staff_data = await get_all_non_employee()
    keyboard = ReplyKeyboardBuilder()
    for data in all_staff_data:
        keyboard.add(
            KeyboardButton(text=f"{data[0].title()} {data[1].title() or ""}")
        )
    return keyboard.adjust(1).as_markup(resize_keyboard=True)


async def check_dir():
    """
    Функция для составления клавиатуры со всеми директорами
    :return:
    """
    all_dir_data = await get_all_dir()
    keyboard = ReplyKeyboardBuilder()
    for data in all_dir_data:
        keyboard.add(
            KeyboardButton(text=f"{data[0].title()} {data[1].title()}")
        )
    return keyboard.adjust(1).as_markup(resize_keyboard=True)


async def check_empl():
    """
    Функция составления клавиатуры со всеми работниками
    :return:
    """
    all_empl_data = await get_all_emp()
    keyboard = ReplyKeyboardBuilder()
    for data in all_empl_data:
        keyboard.add(
            KeyboardButton(text=f"{data[0].title()} {data[1].title()}")
        )
    return keyboard.adjust(1).as_markup(resize_keyboard=True)


async def check_job():
    """
    Функция составления клавиатуры со всеми видами работы
    :return:
    """
    all_job_data = await get_all_jobs()
    keyboard = ReplyKeyboardBuilder()
    for data in all_job_data:
        keyboard.add(KeyboardButton(text=data))
    return keyboard.adjust(1).as_markup(resize_keyboard=True)


async def check_del_staff():
    """
    Функция составления клавиатуры со всеми забаненными пользователями
    :return:
    """
    all_del_staff_data = await get_all_dell()
    keyboard = ReplyKeyboardBuilder()
    for data in all_del_staff_data:
        keyboard.add(
            KeyboardButton(text=f"{data[0].title()} {data[1].title()}")
        )
    return keyboard.adjust(1).as_markup(resize_keyboard=True)
