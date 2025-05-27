from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.func.data_func import get_all_proc_jobs

router_in_process = Router()


@router_in_process.message(Command("in_process"))
async def proc_init(message: Message, state: FSMContext):
    await state.clear()
    proc = await get_all_proc_jobs()
    if proc:
        await message.answer("В процессе работы следующие заявки:")
        for job in proc:
            await message.reply(
                f"Заявка № {job[0]}\n"
                f"Тип работы: {job[1].capitalize()}\n"
                f"Организация: {job[2].capitalize()}\n"
                f"Время поступления заявки: {job[3]}\n"
                f"Сотрудник, вполняющий заявку: {job[4].title()} {job[5].title()}\n"
            )
    else:
        await message.reply(
            "В данный момент нет действующих заявок.",
            reply_markup=ReplyKeyboardRemove(),
        )
