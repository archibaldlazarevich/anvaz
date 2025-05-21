from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


from src.database.func.data_func import get_all_emp

router_emp_number = Router()


@router_emp_number.message(Command("number_emp"))
async def add_dir_init(message: Message):
    employees = await get_all_emp()
    await message.reply(f"В базе данных всего {len(employees)} рабочих")
