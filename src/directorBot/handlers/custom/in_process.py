from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.database.data_func import get_all_proc_jobs, get_all_dir_id

router_in_process = Router()


@router_in_process.message(Command("in_process"))
async def proc_init(message: Message):
    proc = await get_all_proc_jobs()
    if len(proc) != 0:
        await message.answer("В процессе работы следующие заявки:")
        for job in proc:
            await message.reply(
                f"Заявка № {job[0]}\n"
                f"Тип работы: {job[1]}\n"
                f"Организация: {job[2]}\n"
                f"Время поступления заявки: {job[3]}\n"
                f"Сотрудник, вполняющий заявку: {job[4].title()} {job[5].title()}\n"
            )
