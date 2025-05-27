from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.func.data_func import (
    get_all_company,
)

router_company_list = Router()


@router_company_list.message(Command("company_list"))
async def address_list(message: Message, state: FSMContext):
    await state.clear()
    company_data = await get_all_company()
    if company_data:
        await message.reply(
            "В базе данных находятся следующие компании:",
            reply_markup=ReplyKeyboardRemove(),
        )
        for company in company_data:
            await message.reply(
                text=company.capitalize(), reply_markup=ReplyKeyboardRemove()
            )
    else:
        await message.reply(
            "Список активных компаний пуст.",
            reply_markup=ReplyKeyboardRemove(),
        )
