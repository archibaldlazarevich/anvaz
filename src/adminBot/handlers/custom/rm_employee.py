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


async def send_empl(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    await message.reply("Выберите из списка:", reply_markup=repl_data[1])


@router_rm_employee.message(Command("rm_employee"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.clear()
    check_empl_mark = await rep.check_empl()
    if check_empl_mark:
        await state.set_state(RmEm.init)
        await state.update_data(init=check_empl_mark)
        await send_empl(message=message, state=state)
    else:
        await message.reply(
            "В базе данных нет действующих работников",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_rm_employee.message(RmEm.init)
async def add_dir_choice(message: Message, state: FSMContext):
    empl_data = await state.get_value("init")
    if message.text in empl_data[0]:
        await state.clear()
        name, surname = message.text.split()
        await rm_employee(name=name.lower(), surname=surname.lower())
        await message.reply(
            f"Работник {name} {surname} переведен в разряд пользователей",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply("Выберите данные из списка!!!")
