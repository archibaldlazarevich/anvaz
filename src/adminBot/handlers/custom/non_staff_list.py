from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.func.data_func import get_all_non_employee

router_non_staff_list = Router()


@router_non_staff_list.message(Command("non_staff_list"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.clear()
    non_staff = await get_all_non_employee()
    if non_staff:
        await message.reply(
            "В базе данных находятся следующие пользователи:",
            reply_markup=ReplyKeyboardRemove(),
        )
        for user in non_staff:
            await message.answer(f"{user[0]} {user[1]}")
    else:
        await message.reply(
            "В базе данных нет пользователей.",
            reply_markup=ReplyKeyboardRemove(),
        )
