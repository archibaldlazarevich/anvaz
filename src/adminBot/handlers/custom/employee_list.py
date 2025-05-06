from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


from src.adminBot.middlewares.middlewares import TestMiddleware
from src.database.data_func import get_all_emp

router_emp_list = Router()

router_emp_list.message.outer_middleware(TestMiddleware())


@router_emp_list.message(Command("emp_list"))
async def add_dir_init(message: Message):
    employees = await get_all_emp()
    await message.reply('В базе данных находятся следующие рабочие:')
    for employee in employees:
        await message.answer(f'{employee[0]} {employee[1]}')
