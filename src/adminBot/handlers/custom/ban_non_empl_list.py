from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.func.data_func import get_all_del_non_employee

router_ban_non_empl_list = Router()


@router_ban_non_empl_list.message(Command("ban_non_empl_list"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.clear()
    employees = await get_all_del_non_employee()
    if employees:
        await message.reply(
            "В базе данных находятся следующие неактивные пользователи:",
            reply_markup=ReplyKeyboardRemove(),
        )
        for employee in employees:
            await message.answer(
                f"{employee[0].title()} {employee[1].title()}"
            )
    else:
        await message.reply(
            "В базе данных нет неактивных пользователей",
            reply_markup=ReplyKeyboardRemove(),
        )
