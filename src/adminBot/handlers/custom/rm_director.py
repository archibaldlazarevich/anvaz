from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.adminBot.middlewares.middlewares import TestMiddleware
import src.adminBot.keyboards.reply as rep
from src.database.func.data_func import rm_direct

router_rm_directors = Router()

router_rm_directors.message.outer_middleware(TestMiddleware())


class RmDir(StatesGroup):
    init = State()


@router_rm_directors.message(Command("rm_director"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.set_state(RmDir.init)
    await message.reply(
        "Для удаления из базы данных, выберите начальника из списка",
        reply_markup=await rep.check_dir(),
    )


@router_rm_directors.message(RmDir.init)
async def add_dir_choice(message: Message, state: FSMContext):
    await state.clear()
    name, surname = message.text.split()
    await rm_direct(name=name.lower(), surname=surname.lower())
    await message.reply(
        f"Начальник {name} {surname} переведен в разряд пользователей",
        reply_markup=ReplyKeyboardRemove(),
    )
