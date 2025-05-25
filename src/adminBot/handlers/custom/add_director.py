from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


import src.adminBot.keyboards.reply as rep
from src.database.func.data_func import add_direct

router_add_directors = Router()


class AddDir(StatesGroup):
    init = State()


async def add_dir_func(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    await message.reply("Выберите из списка:", reply_markup=repl_data[1])


@router_add_directors.message(Command("add_director"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.clear()
    check_staff_mark = await rep.check_staff()
    if check_staff_mark:
        await state.set_state(AddDir.init)
        await state.update_data(init=check_staff_mark)
        await add_dir_func(message=message, state=state)
    else:
        await message.reply(
            "Нет свободных пользователей.", reply_markup=ReplyKeyboardRemove()
        )


@router_add_directors.message(AddDir.init)
async def add_dir_choice(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    if message.text in repl_data[0]:
        name, surname = message.text.split()
        await add_direct(name=name.lower(), surname=surname.lower())
        await message.reply(
            f"Пользователь {name} {surname} переведён в статус начальника.",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await add_dir_func(message=message, state=state)
