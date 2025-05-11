from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.database.data_func import (
    get_busy_empl,
)


async def key_busy_employee():
    """
    Функция для составления клавиатуры с занятыми работниками
    :return:
    """
    all_busy_staff = await get_busy_empl()
    keyboard = ReplyKeyboardBuilder()
    for data in all_busy_staff:
        keyboard.add(
            KeyboardButton(text=f"{data[0].title()} {data[1].title()}")
        )
    return keyboard.adjust(1).as_markup(resize_keyboard=True, one_time_keyboard=True,)


employee = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Все сотрудники")],
        [KeyboardButton(text="Определённый сотрудник")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
