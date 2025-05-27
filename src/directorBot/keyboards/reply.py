from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.database.func.data_func import (
    get_busy_empl,
    get_all_job_by_empl,
    get_busy_empl_without_spec_empl,
    get_job_by_empl,
    get_all_emp,
)


async def key_busy_employee():
    """
    Функция для составления клавиатуры с занятыми работниками
    :return:
    """
    all_busy_staff = await get_busy_empl()
    keyboard = ReplyKeyboardBuilder()
    if all_busy_staff:
        all_data = [
            f"{data[0].title()} {data[1].title()}" for data in all_busy_staff
        ]
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False


async def get_all_empl():
    """
    Функция, для составления клавиатуру со всеми работниками
    :return:
    """
    all_busy_staff = await get_all_emp()
    keyboard = ReplyKeyboardBuilder()
    if all_busy_staff:
        all_data = [
            f"{data[0].title()} {data[1].title()}" for data in all_busy_staff
        ]
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False


async def get_job_by_empl_name(name: str, surname: str):
    """
    Функция, возращает клавиатуру с работами сотруника
    :param name:
    :param surname:
    :return:
    """
    job_data = await get_job_by_empl(
        name=name.lower(), surname=surname.lower()
    )
    if job_data:
        keyboard = ReplyKeyboardBuilder()
        all_data = [
            f"Заявка № {data[0]}\n"
            f"Организация: {data[1].capitalize()}\n"
            f"Адреc: {data[2].capitalize()}"
            for data in job_data
        ]
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False


async def key_busy_employee_without_spec(name: str, surname: str):
    """
    Функция, которая возвращает клавиатуру с работниками без переданного
    :param name:
    :param surname:
    :return:
    """
    all_busy_staff = await get_busy_empl_without_spec_empl(
        name=name, surname=surname
    )
    keyboard = ReplyKeyboardBuilder()
    if all_busy_staff:
        all_data = [
            f"{data[0].title()} {data[1].title()}" for data in all_busy_staff
        ]
        for data in all_data:

            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return False


# async def check_task(empl_id: int):
#     """
#     Функция, которая возвращает клавиатуру, если есть незакрытые заявки у работника
#     :param empl_id:
#     :return:
#     """
#     all_jobs = await get_all_job_by_empl(empl_id=empl_id)
#     if all_jobs:
#         keyboard = ReplyKeyboardBuilder()
#         for data in all_jobs:
#             keyboard.add(
#                 KeyboardButton(
#                     text=f"Заявка № {data[0]}\n"
#                     f"Организация {data[1]}\n"
#                     f"Адрес {data[2]}"
#                 )
#             )
#         return keyboard.adjust(1).as_markup(
#             resize_keyboard=True,
#             one_time_keyboard=True,
#         )
#     return False


employee = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Все сотрудники")],
        [KeyboardButton(text="Определённый сотрудник")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


async def task_choice():
    """
    Функция, которая возвращает клавиатуру, для выбора типа заявки
    :return:
    """
    all_data = ["Все заявки", "Активные заявки", "Завершенные заявки"]
    keyboard = ReplyKeyboardBuilder()
    for data in all_data:
        keyboard.add(KeyboardButton(text=data))
    markup = keyboard.adjust(1).as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return all_data, markup


async def time_choice():
    """
    Функция, которая возвращает клавиатуру, для выбора типа заявки
    :return:
    """
    all_data = ["За сутки", "За неделю", "За месяц", "За все время"]
    keyboard = ReplyKeyboardBuilder()
    for data in all_data:
        keyboard.add(KeyboardButton(text=data))
    markup = keyboard.adjust(1).as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return all_data, markup
