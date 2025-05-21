from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import src.adminBot.keyboards.reply as rep
from src.database.func.data_func import rm_employee

router_rm_employee = Router()


class RmEm(StatesGroup):
    init = State()


@router_rm_employee.message(Command("rm_employee"))
async def add_dir_init(message: Message, state: FSMContext):
    check_empl_mark = await rep.check_empl()
    if check_empl_mark:
        await state.set_state(RmEm.init)
        await message.reply(
            "Для удаления из базы данных, выберите работника из списка",
            reply_markup=check_empl_mark,
        )
    else:
        await message.reply("В базе данных нет действующих работников")


@router_rm_employee.message(RmEm.init)
async def add_dir_choice(message: Message, state: FSMContext):
    await state.clear()
    name, surname = message.text.split()
    await rm_employee(name=name.lower(), surname=surname.lower())
    await message.reply(
        f"Работник {name} {surname} переведен в разряд пользователей",
        reply_markup=ReplyKeyboardRemove(),
    )
