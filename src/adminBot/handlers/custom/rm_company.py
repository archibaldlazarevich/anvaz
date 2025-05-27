from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.func.data_func import (
    check_all_company,
    rm_company,
)
import src.adminBot.keyboards.reply as rep

router_company_rm = Router()


class CompRm(StatesGroup):
    init: State = State()
    comp: State = State()


async def send_company(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    await message.reply("Выберите из списка:", reply_markup=repl_data[1])


@router_company_rm.message(Command("rm_company"))
async def address_rm(message: Message, state: FSMContext):
    await state.clear()
    check_company_rep = await rep.check_company()
    if check_company_rep:
        await state.set_state(CompRm.init)
        await state.update_data(init=check_company_rep)
        await send_company(message=message, state=state)
    else:
        await message.reply(
            "В базе данных нет действующих компаний,"
            " пожалуйста создайте компанию командой:\n/add_company",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_company_rm.message(CompRm.init)
async def check_company_command(message: Message, state: FSMContext):
    company_name = message.text.lower()
    check_company_data = await check_all_company(company_name=company_name)
    if check_company_data == 3:
        await message.reply(
            "Данная компания уже добавлена в базу данных, "
            "чтобы сделать ее активной, воспользуйтесь командой:\n/return_company",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
    elif check_company_data:
        await rm_company(company_name=company_name)
        await message.reply(
            f"Компания {message.text} переведена в список неактивных,"
            f" все адреса данной компании также неактивны",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
    else:
        await message.reply(
            "Пожалуйста, выберите данные из списка!!!",
            reply_markup=ReplyKeyboardRemove(),
        )
        await send_company(message=message, state=state)
