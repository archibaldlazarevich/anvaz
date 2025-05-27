from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.func.data_func import (
    check_all_company,
    check_address_for_company,
    rm_address,
)
import src.adminBot.keyboards.reply as rep

router_address_rm = Router()


class AdRm(StatesGroup):
    init: State = State()
    address: State = State()


async def send_company(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    await message.reply("Выберите из списка:", reply_markup=repl_data[1])


async def send_address(message: Message, state: FSMContext, company_name: str):
    address_company = await rep.check_address(company_name=company_name)
    if address_company:
        await state.set_state(AdRm.address)
        await message.reply(
            "Выберите адрес из списка:", reply_markup=address_company
        )
    else:
        await message.reply(
            "Нет доступных адресов для этой компании.",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_address_rm.message(Command("rm_address"))
async def address_rm(message: Message, state: FSMContext):
    await state.clear()
    check_company_rep = await rep.check_company()
    if check_company_rep:
        await state.set_state(AdRm.init)
        await state.update_data(init=check_company_rep)
        await send_company(message=message, state=state)
    else:
        await message.reply(
            "В базе данных нет действующих компаний,"
            " пожалуйста создайте компанию командой:\n/add_company",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_address_rm.message(AdRm.init)
async def check_company_command(message: Message, state: FSMContext):
    company_name = message.text.lower()
    check_company_data = await check_all_company(company_name=company_name)
    if check_company_data == 3:
        await message.reply(
            "Данная компания уже добавлена в базу данных, "
            "чтобы сделать ее активной, воспользуйтесь командой:\n/return_company",
            reply_markup=ReplyKeyboardRemove(),
        )
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


@router_address_rm.message(AdRm.address)
async def rm_address_cancel(message: Message, state: FSMContext):
    address = message.text.lower()
    company_name = await state.get_value("init")
    check_address = await check_address_for_company(
        company_name=company_name, address=address
    )
    if not check_address:
        await message.reply(
            "Выберите адрес из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_address(
            message=message, state=state, company_name=company_name
        )
    else:
        await rm_address(company_name=company_name, address=address)
        await state.clear()
        await message.reply(
            "Адрес переведен в список неактивных.",
            reply_markup=ReplyKeyboardRemove(),
        )
