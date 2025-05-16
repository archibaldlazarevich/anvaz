from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.adminBot.middlewares.middlewares import TestMiddleware
import src.adminBot.keyboards.reply as rep
from src.database.func.data_func import add_direct

router_add_directors = Router()

router_add_directors.message.outer_middleware(TestMiddleware())


class AddDir(StatesGroup):
    init = State()


@router_add_directors.message(Command("add_director"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.set_state(AddDir.init)
    await message.reply(
        "Выберите из списка", reply_markup=await rep.check_staff()
    )


@router_add_directors.message(AddDir.init)
async def add_dir_choice(message: Message, state: FSMContext):
    await state.clear()
    name, surname = message.text.split()
    await add_direct(name=name.lower(), surname=surname.lower())
    await message.reply(
        f"Пользователь {name} {surname} переведён в статус начальника",
        reply_markup=ReplyKeyboardRemove(),
    )
