from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import src.adminBot.keyboards.reply as rep
from src.database.func.data_func import return_del

router_return_non_staff = Router()


class RetNonStaff(StatesGroup):
    init = State()


@router_return_non_staff.message(Command("return_non_staff"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.clear()
    repl_data = await rep.check_del_staff()
    if repl_data:
        await state.set_state(RetNonStaff.init)
        await message.reply(
            "Для возврата в статус пользователя, выберите аккаунт из списка:",
            reply_markup=await rep.check_del_staff(),
        )
    else:
        await message.reply(
            "В данный момент неактивных пользователей нет в базе данных.",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_return_non_staff.message(RetNonStaff.init)
async def add_dir_choice(message: Message, state: FSMContext):
    name, surname = message.text.split()
    if await return_del(name=name.lower(), surname=surname.lower()):
        await message.reply(
            f"Пользователь {name} {surname} переведен в неактивные.",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply(
            "Вы ввели несуществующего пользователя,"
            " пожалуйста выберите пользователя из списка.",
            reply_markup=ReplyKeyboardRemove(),
        )
    await state.clear()
