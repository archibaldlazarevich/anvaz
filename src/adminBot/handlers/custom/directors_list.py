from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.func.data_func import get_all_dir

router_dir_list = Router()


@router_dir_list.message(Command("dir_list"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.clear()
    directors = await get_all_dir()
    if directors:
        await message.reply(
            "В базе данных находятся следующие начальники:",
            reply_markup=ReplyKeyboardRemove(),
        )
        for dir_ in directors:
            await message.answer(f"{dir_[0].title()} {dir_[1].title()}")
    else:
        await message.reply(
            "В базе данных нет действующий начальников",
            reply_markup=ReplyKeyboardRemove(),
        )
