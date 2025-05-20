from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.database.func.data_func import get_all_job_by_empl

router_check_task = Router()


@router_check_task.message(Command("check"))
async def check_task(message: Message):
    result = await get_all_job_by_empl(empl_id=message.from_user.id)
    if result:
        for data in result:
            await message.answer(
                f"Заявка № {data[0]}\n"
                f"Организация: {data[1].capitalize()}\n"
                f"Адрес: {data[2].capitalize()}\n"
                f"Вид работы: {data[3].capitalize()}"
            )
    else:
        await message.reply("У вас нет активных заявок")
