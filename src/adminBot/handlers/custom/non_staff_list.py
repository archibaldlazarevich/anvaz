from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


from src.adminBot.middlewares.middlewares import TestMiddleware
from src.database.data_func import get_all_non_employee

router_non_staff_list = Router()

router_non_staff_list.message.outer_middleware(TestMiddleware())


@router_non_staff_list.message(Command("non_staff_list"))
async def add_dir_init(message: Message):
    non_staff = await get_all_non_employee()
    await message.reply("В базе данных находятся следующие пользователи:")
    for user in non_staff:
        await message.answer(f"{user[0]} {user[1]}")
