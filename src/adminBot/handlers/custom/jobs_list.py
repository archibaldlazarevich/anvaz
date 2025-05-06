from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


from src.adminBot.middlewares.middlewares import TestMiddleware
from src.database.data_func import get_all_jobs

router_jobs_list = Router()

router_jobs_list.message.outer_middleware(TestMiddleware())


@router_jobs_list.message(Command("jobs_list"))
async def add_dir_init(message: Message):
    jobs = await get_all_jobs()
    await message.reply('В базе данных находятся следующие виды работ:')
    for job in jobs:
        await message.answer(f'{job}')
