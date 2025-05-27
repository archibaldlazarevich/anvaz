from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import src.adminBot.keyboards.reply as rep
from src.database.func.data_func import return_del_company

router_return_company = Router()


class RetComp(StatesGroup):
    init = State()


@router_return_company.message(Command("return_company"))
async def return_company(message: Message, state: FSMContext):
    await state.clear()
    repl_data = await rep.check_company_del()
    if repl_data:
        await state.set_state(RetComp.init)
        await message.reply(
            "Для возврата в активные компании, выберите неоходимую списка",
            reply_markup=repl_data,
        )
    else:
        await message.reply(
            "В данный момент неактивных компаний нет в базе данных.",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_return_company.message(RetComp.init)
async def return_company_choice(message: Message, state: FSMContext):
    if await return_del_company(company_name=message.text.lower()):
        await message.reply(
            f"Компания '{message.text.capitalize()}' переведена в активные, и все адреса, "
            f"привязанные к этой компании вовращены в активные",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply(
            "Введеная вами компания отсутствует в базе данный, пожалуйста выберите нужную из списка.",
            reply_markup=ReplyKeyboardRemove(),
        )
    await state.clear()