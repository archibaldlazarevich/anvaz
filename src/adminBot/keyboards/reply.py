from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.database.func.data_func import (
    get_all_non_employee,
    get_all_dir,
    get_all_emp,
    get_all_jobs,
    get_all_dell,
    get_all_dell_job,
    get_all_company_name,
    check_active_address_for_company,
    get_all_del_company,
    check_ban_address_for_company,
)


async def check_staff():
    """
    Функция для составления клавиатуры со всем персоналом
    :return:
    """
    all_staff_data = await get_all_non_employee()
    keyboard = ReplyKeyboardBuilder()
    if all_staff_data:
        all_data = [
            f"{data[0].title()} {data[1].title()}" for data in all_staff_data
        ]
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False


async def check_address(company_name: str):
    """
    Функция возвращает клавиатуру, если существуют активные адреса для данной компании
    :return:
    """
    all_address_data = await check_active_address_for_company(
        company_name=company_name
    )
    keyboard = ReplyKeyboardBuilder()
    if all_address_data:
        for data in all_address_data:
            keyboard.add(KeyboardButton(text=f"{data.capitalize()}"))
        return keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    return False


async def check_ban_address(company_name: str):
    """
    Функция возвращает клавиатуру, если существуют неактивные адреса для данной компании
    :return:
    """
    all_address_data = await check_ban_address_for_company(
        company_name=company_name
    )
    keyboard = ReplyKeyboardBuilder()
    if all_address_data:
        for data in all_address_data:
            keyboard.add(KeyboardButton(text=f"{data.capitalize()}"))
        return keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    return False


async def check_company():
    """
    Функция для составления клавиатуры со всеми дейстующими компаниями
    :return:
    """
    all_company_data = await get_all_company_name()
    keyboard = ReplyKeyboardBuilder()
    if all_company_data:
        all_data = [data for data in all_company_data]
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False


async def check_dir():
    """
    Функция для составления клавиатуры со всеми директорами
    :return:
    """
    all_dir_data = await get_all_dir()
    keyboard = ReplyKeyboardBuilder()
    if all_dir_data:
        all_data = [
            f"{data[0].title()} {data[1].title()}" for data in all_dir_data
        ]
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False


async def check_empl():
    """
    Функция составления клавиатуры со всеми работниками
    :return:
    """
    all_empl_data = await get_all_emp()
    keyboard = ReplyKeyboardBuilder()
    if all_empl_data:
        all_data = [
            f"{data[0].title()} {data[1].title()}" for data in all_empl_data
        ]
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False


async def check_job():
    """
    Функция составления клавиатуры со всеми видами работы
    :return:
    """
    all_job_data = await get_all_jobs()
    keyboard = ReplyKeyboardBuilder()
    if all_job_data:
        all_data = [data.capitalize() for data in all_job_data]
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False


async def check_del_staff():
    """
    Функция составления клавиатуры со всеми забаненными пользователями
    :return:
    """
    all_del_staff_data = await get_all_dell()
    keyboard = ReplyKeyboardBuilder()
    if all_del_staff_data:
        for data in all_del_staff_data:
            keyboard.add(
                KeyboardButton(text=f"{data[0].title()} {data[1].title()}")
            )
        return keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    return False


async def check_job_del():
    """
    Функция составления клавиатуры со всеми забаненными видами работ
    :return:
    """
    all_del_staff_data = await get_all_dell_job()
    keyboard = ReplyKeyboardBuilder()
    if all_del_staff_data:
        for data in all_del_staff_data:
            keyboard.add(KeyboardButton(text=f"{data.capitalize()}"))
        return keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    return False


async def check_company_del():
    """
    Функция составления клавиатуры со всеми забаненными компаниями
    :return:
    """
    all_del_staff_data = await get_all_del_company()
    keyboard = ReplyKeyboardBuilder()
    if all_del_staff_data:
        for data in all_del_staff_data:
            keyboard.add(KeyboardButton(text=f"{data.capitalize()}"))
        return keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    return False
