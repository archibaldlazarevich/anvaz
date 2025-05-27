from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.database.func.data_func import (
    get_all_job_type,
    get_all_company_name,
    get_all_job_by_empl,
    get_address_by_empl_id_for_update,
    get_all_company_name_without_spec, get_all_active_company_name,
)


async def get_all_job_type_reply():
    """
    Функция для составления клавиатуры с видами работ
    :return:
    """
    all_job_type = await get_all_job_type()
    if all_job_type:
        keyboard = ReplyKeyboardBuilder()
        all_data = [data.capitalize() for data in all_job_type]
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False


async def get_company_name_mark():
    """
    Функция возвращает клавиатуру если есть названия компаний в бд и False при их отсутствии
    :return:
    """
    all_company_name = await get_all_active_company_name()
    if all_company_name:
        all_data = [data.capitalize() for data in all_company_name]
        keyboard = ReplyKeyboardBuilder()
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False


async def get_company_name_mark_without_spec(company_name: str):
    """
    Функция возвращает клавиатуру если есть названия компаний в бд и False при их отсутствии
    :return:
    """
    all_company_name = await get_all_company_name_without_spec(
        company_name=company_name
    )
    if all_company_name:
        all_data = [data.capitalize() for data in all_company_name]
        keyboard = ReplyKeyboardBuilder()
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
    Функция возвращает клавиатуру есть есть адреса объектов по базе данных и False при их отсутствии
    :return:
    """
    all_address_by_company = await get_address_by_empl_id_for_update(
        company_name=company_name
    )
    if all_address_by_company:
        all_data = [data.capitalize() for data in all_address_by_company]
        keyboard = ReplyKeyboardBuilder()
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False


async def check_task(empl_id: int):
    """
    Функция, которая возвращает клавиатуру, если есть незакрытые заявки у работника
    :param empl_id:
    :return:
    """
    all_jobs = await get_all_job_by_empl(empl_id=empl_id)
    if all_jobs:
        all_data = [
            f"Заявка № {data[0]}\n"
            f"Организация: {data[1].capitalize()}\n"
            f"Адрес: {data[2].capitalize()}"
            for data in all_jobs
        ]
        keyboard = ReplyKeyboardBuilder()
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False


# company_choose_rep = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="Изменить заказчика")],
#         [KeyboardButton(text="Оставить старые данные")],
#     ],
#     resize_keyboard=True,
#     one_time_keyboard=True,
# )
#
# address_choose_rep = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="Поменять адрес")],
#         [KeyboardButton(text="Оставить старые данные")],
#     ],
#     resize_keyboard=True,
#     one_time_keyboard=True,
# )
#
# jobs_choose_rep = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="Поменять вид работы")],
#         [KeyboardButton(text="Оставить старые данные")],
#     ],
#     resize_keyboard=True,
#     one_time_keyboard=True,
# )


async def check_address_for_update(company_name: str):
    """
    Функция возвращает клавиатуру если есть адреса объектов по базе данных и False при их отсутствии
    :return:
    """
    all_address_by_company = await get_address_by_empl_id_for_update(
        company_name=company_name
    )
    if all_address_by_company:
        all_data = [data.capitalize() for data in all_address_by_company]
        keyboard = ReplyKeyboardBuilder()
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False
