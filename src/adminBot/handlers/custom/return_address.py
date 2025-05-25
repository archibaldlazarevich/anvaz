from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import src.adminBot.keyboards.reply as rep
from src.database.func.data_func import (
    return_address,
    check_all_company,
    check_if_ban_address_for_company,
)

router_return_address = Router()


class RetAddress(StatesGroup):
    init = State()
    address = State()


async def send_company(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    await message.reply("Выберите из списка:", reply_markup=repl_data[1])


async def send_address(message: Message, state: FSMContext, company_name: str):
    address_company = await rep.check_ban_address(company_name=company_name)
    if address_company:
        await state.set_state(RetAddress.address)
        await message.reply(
            "Выберите адрес из списка:", reply_markup=address_company
        )
    else:
        await message.reply(
            "Нет доступных адресов для этой компании",
            reply_markup=ReplyKeyboardRemove(),
        )
    await state.clear()


@router_return_address.message(Command("return_address"))
async def return_company(message: Message, state: FSMContext):
    await state.clear()
    repl_data = await rep.check_company()
    if repl_data:
        await state.set_state(RetAddress.init)
        await state.update_data(init=repl_data)
        await send_company(message=message, state=state)
    else:
        await message.reply(
            "В данный момент компаний нет в базе данных.",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_return_address.message(RetAddress.init)
async def return_company_choice(message: Message, state: FSMContext):
    company_name = message.text.lower()
    check_company_data = await check_all_company(company_name=company_name)
    if check_company_data == 3:
        await message.reply(
            "Данная компания уже добавлена в базу данных, "
            "чтобы сделать ее активной, воспользуйтесь командой \n/return_company",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
    elif check_company_data:
        await state.update_data(init=company_name)
        await send_address(
            message=message, state=state, company_name=company_name
        )
    else:
        await message.reply(
            "Пожалуйста, выберите данные из списка!!!",
            reply_markup=ReplyKeyboardRemove(),
        )
        await send_company(message=message, state=state)


@router_return_address.message(RetAddress.address)
async def rm_address_cancel(message: Message, state: FSMContext):
    address = message.text.lower()
    company_name = await state.get_value("init")
    check_address = await check_if_ban_address_for_company(
        company_name=company_name, address=address
    )
    if not check_address:
        await message.reply(
            "Выберите адрес из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_address(
            message=message, state=state, company_name=company_name
        )
    if check_address:
        await return_address(company_name=company_name, address=address)
        await message.reply(
            "Адрес переведен в активные", reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
