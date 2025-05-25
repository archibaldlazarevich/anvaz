from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.func.data_func import get_all_jobs

router_jobs_list = Router()


@router_jobs_list.message(Command("jobs_list"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.clear()
    jobs = await get_all_jobs()
    if jobs:
        await message.reply(
            "В базе данных находятся следующие виды работ:",
            reply_markup=ReplyKeyboardRemove(),
        )
        for job in jobs:
            await message.answer(f"{job.capitalize()}")
    else:
        await message.reply(
            "В базе данных нет добавленных видов работ",
            reply_markup=ReplyKeyboardRemove(),
        )
