from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.database.func.data_func import (
    get_all_busy_empl,
    check_if_have_busy_amp,
)

router_dir_busy_emp = Router()


@router_dir_busy_emp.message(Command("busy"))
async def busy_init(message: Message):
    result = await check_if_have_busy_amp()
    if result:
        all_empl = await get_all_busy_empl()
        for empl in all_empl:
            await message.reply(
                f"Сотрудник: {empl[0].title()} {empl[1].title()}\n"
                f"Активные заявки: {empl[2]} шт.\n"
            )
    else:
        await message.reply("В данный момент все работники свободны")
