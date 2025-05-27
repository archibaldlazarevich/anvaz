from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import src.adminBot.keyboards.reply as rep
from src.adminBot.keyboards.reply import check_dir
from src.database.func.data_func import rm_direct

router_rm_directors = Router()


class RmDir(StatesGroup):
    init = State()


async def send_dir(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    await message.reply("Выберите из списка:", reply_markup=repl_data[1])


@router_rm_directors.message(Command("rm_director"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.clear()
    check_dir_mark = await rep.check_dir()
    if check_dir_mark:
        await state.set_state(RmDir.init)
        await state.update_data(init=check_dir_mark)
        await send_dir(message=message, state=state)
    else:
        await message.reply(
            "Нет начальников в базе данных.",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_rm_directors.message(RmDir.init)
async def add_dir_choice(message: Message, state: FSMContext):
    dir_data = await state.get_value("init")
    if message.text in dir_data[0]:
        await state.clear()
        name, surname = message.text.split()
        await rm_direct(name=name.lower(), surname=surname.lower())
        await message.reply(
            f"Начальник {name} {surname} переведен в разряд пользователей.",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply("Выберите данные из списка!!!")
