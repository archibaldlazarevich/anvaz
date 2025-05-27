from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import src.adminBot.keyboards.reply as rep
from src.database.func.data_func import rm_non_staff

router_rm_non_staff = Router()


class RmNonStaff(StatesGroup):
    init = State()


async def send_non_staff(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    await message.reply("Выберите из списка:", reply_markup=repl_data[1])


@router_rm_non_staff.message(Command("rm_non_staff"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.clear()
    rm_mark = await rep.check_staff()
    if rm_mark:
        await state.set_state(RmNonStaff.init)
        await state.update_data(init=rm_mark)
        await send_non_staff(message=message, state=state)
    else:
        await message.reply(
            "В базе данных нет свободных пользователей.",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_rm_non_staff.message(RmNonStaff.init)
async def add_dir_choice(message: Message, state: FSMContext):
    job_data = await state.get_value("init")
    if message.text in job_data[0]:
        await state.clear()
        name, surname = message.text.split()
        await rm_non_staff(name=name.lower(), surname=surname.lower())
        await message.reply(
            f"Пользователь {name} {surname} переведен в неактивные.",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply("Выберите данные из списка!!!")
