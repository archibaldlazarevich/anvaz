from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.func.data_func import get_all_emp

router_emp_list = Router()


@router_emp_list.message(Command("emp_list"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.clear()
    employees = await get_all_emp()
    if employees:
        await message.reply(
            "В базе данных находятся следующие рабочие:",
            reply_markup=ReplyKeyboardRemove(),
        )
        for employee in employees:
            await message.answer(
                f"{employee[0].title()} {employee[1].title()}"
            )
    else:
        await message.reply(
            "В базе данных нет действующих работников.",
            reply_markup=ReplyKeyboardRemove(),
        )
