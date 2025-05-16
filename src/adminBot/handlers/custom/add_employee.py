from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.adminBot.middlewares.middlewares import TestMiddleware
import src.adminBot.keyboards.reply as rep
from src.database.func.data_func import add_employee

router_add_empl = Router()

router_add_empl.message.outer_middleware(TestMiddleware())


class AddEm(StatesGroup):
    init = State()


@router_add_empl.message(Command("add_employee"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.set_state(AddEm.init)
    await message.reply(
        "Выберите из списка", reply_markup=await rep.check_staff()
    )


@router_add_empl.message(AddEm.init)
async def add_dir_choice(message: Message, state: FSMContext):
    await state.clear()
    name, surname = message.text.split()
    await add_employee(name=name.lower(), surname=surname.lower())
    await message.reply(
        f"Пользователь {name} {surname} переведен в статус работника",
        reply_markup=ReplyKeyboardRemove(),
    )
