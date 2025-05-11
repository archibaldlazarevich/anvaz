from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.adminBot.middlewares.middlewares import TestMiddleware
import src.adminBot.keyboards.reply as rep
from src.database.data_func import return_del

router_return_non_staff = Router()

router_return_non_staff.message.outer_middleware(TestMiddleware())


class RmNonStaff(StatesGroup):
    init = State()


@router_return_non_staff.message(Command("return_non_staff"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.set_state(RmNonStaff.init)
    await message.reply(
        "Для возврата в статус пользователя, выберите аккаунт из списка",
        reply_markup=await rep.check_del_staff(),
    )


@router_return_non_staff.message(RmNonStaff.init)
async def add_dir_choice(message: Message, state: FSMContext):
    await state.clear()
    name, surname = message.text.split()
    await return_del(name=name.lower(), surname=surname.lower())
    await message.reply(
        f"Пользователь {name} {surname} переведен в неактивные",
        reply_markup=ReplyKeyboardRemove(),
    )
