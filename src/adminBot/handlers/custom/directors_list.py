from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.database.func.data_func import get_all_dir

router_dir_list = Router()


@router_dir_list.message(Command("dir_list"))
async def add_dir_init(message: Message):
    directors = await get_all_dir()
    if len(directors) != 0:
        await message.reply("В базе данных находятся следующие начальники:")
        for dir_ in directors:
            await message.answer(f"{dir_[0].title()} {dir_[1].title()}")
    else:
        await message.reply("В базе данных нет действующий начальников")
