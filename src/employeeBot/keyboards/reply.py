from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.database.func.data_func import (
    get_all_job_type,
    get_all_company_name,
    get_address_by_empl_id,
    get_all_job_by_empl,
    get_address_by_empl_id_for_update,
)


async def get_all_job_type_reply():
    """
    Функция для составления клавиатуры с видами работ
    :return:
    """
    all_job_type = await get_all_job_type()
    keyboard = ReplyKeyboardBuilder()
    for data in all_job_type:
        keyboard.add(KeyboardButton(text=f"{data.title()}"))
    return keyboard.adjust(1).as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )


async def get_company_name_mark():
    """
    Функция возвращает клавиатуру если есть названия компаний в бд и False при их отсутствии
    :return:
    """
    all_company_name = await get_all_company_name()
    if len(all_company_name) != 0:
        keyboard = ReplyKeyboardBuilder()
        for data in all_company_name:
            keyboard.add(KeyboardButton(text=f"{data.title()}"))
        return keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    return False


async def check_address(empl_id: int):
    """
    Функция возвращает клавиатуру есть есть адреса объектов по базе данных и False при их отсутствии
    :return:
    """
    all_address_by_company = await get_address_by_empl_id(empl_id=empl_id)
    if all_address_by_company:
        keyboard = ReplyKeyboardBuilder()
        for data in all_address_by_company:
            keyboard.add(KeyboardButton(text=f"{data.title()}"))
        return keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    return False


async def check_task(empl_id: int):
    """
    Функция, которая возвращает клавиатуру, если есть незакрытые заявки у работника
    :param empl_id:
    :return:
    """
    all_jobs = await get_all_job_by_empl(empl_id=empl_id)
    if all_jobs:
        keyboard = ReplyKeyboardBuilder()
        for data in all_jobs:
            keyboard.add(
                KeyboardButton(
                    text=f"Заявка № {data[0]}\n"
                    f"Организация {data[1]}\n"
                    f"Адрес {data[2]}"
                )
            )
        return keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    return False


company_choose_rep = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Изменить заказчика")],
        [KeyboardButton(text="Оставить старые данные")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

address_choose_rep = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Поменять адрес")],
        [KeyboardButton(text="Оставить старые данные")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

jobs_choose_rep = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Поменять вид работы")],
        [KeyboardButton(text="Оставить старые данные")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


async def check_address_for_update(empl_id: int):
    """
    Функция возвращает клавиатуру если есть адреса объектов по базе данных и False при их отсутствии
    :return:
    """
    all_address_by_company = await get_address_by_empl_id_for_update(
        empl_id=empl_id
    )
    if all_address_by_company:
        keyboard = ReplyKeyboardBuilder()
        for data in all_address_by_company:
            keyboard.add(KeyboardButton(text=f"{data.title()}"))
        return keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    return False
