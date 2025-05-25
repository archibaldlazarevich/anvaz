from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.func.data_func import (
    get_all_address_for_company,
    check_all_company,
)
import src.adminBot.keyboards.reply as rep

router_address_list = Router()


class AdList(StatesGroup):
    init: State = State()


async def send_company(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    await message.reply("Выберите из списка:", reply_markup=repl_data[1])


@router_address_list.message(Command("address_list"))
async def address_list(message: Message, state: FSMContext):
    await state.clear()
    check_company_ = await rep.check_company()
    if check_company_:
        await state.set_state(AdList.init)
        await state.update_data(init=check_company_)
        await send_company(message=message, state=state)
    else:
        await message.reply(
            "В базе данных нет действующих компаний, пожалуйста создайте компанию командой:\n/add_company",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_address_list.message(AdList.init)
async def check_company_command(message: Message, state: FSMContext):
    company_name = message.text.lower()
    check_company_data = await check_all_company(company_name=company_name)
    if check_company_data == 3:
        await message.reply(
            "Данная компания уже добавлена в базу данных, "
            "чтобы сделать ее активной, воспользуйтесь командой \n/return_company",
            reply_markup=ReplyKeyboardRemove(),
        )
    elif check_company_data:
        address_company = await get_all_address_for_company(company_name)
        for address in address_company:
            await message.answer(text=address)
    else:
        await message.reply(
            "Пожалуйста, выберите данные из списка!!!",
            reply_markup=ReplyKeyboardRemove(),
        )
        await send_company(message=message, state=state)
        await state.clear()
