from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


import src.adminBot.keyboards.reply as rep
from src.database.func.data_func import (
    add_new_address,
    check_address_for_company_all,
)

router_add_address = Router()


class AddAddress(StatesGroup):
    init = State()
    create_address = State()


async def send_company(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    await message.reply("Выберите из списка:", reply_markup=repl_data[1])


@router_add_address.message(Command("add_address"))
async def add_address_init(message: Message, state: FSMContext):
    await state.clear()
    check_company_rep = await rep.check_company()
    if check_company_rep:
        await state.set_state(AddAddress.init)
        await state.update_data(init=check_company_rep)
        await send_company(message=message, state=state)
    else:
        await message.reply(
            "В базе данных нет действующих компаний, пожалуйста создайте компанию командой:\n/add_company"
        )


@router_add_address.message(AddAddress.init)
async def check_company_command(message: Message, state: FSMContext):
    company_name = message.text.lower()
    company_data = await state.get_value("init")
    if company_name in company_data[0]:
        await state.set_state(AddAddress.create_address)
        await state.update_data(create_address=message.text.lower())
        await message.reply(
            "Напишите адрес, который требуется добавить в базу данных:",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply(
            "Пожалуйста, выберите данные из списка!!!",
            reply_markup=ReplyKeyboardRemove(),
        )
        await send_company(message=message, state=state)


@router_add_address.message(AddAddress.create_address)
async def add_dir_choice(message: Message, state: FSMContext):
    address = message.text.lower()
    if len(address) > 2:
        company_name = await state.get_value("create_address")
        check_address = await check_address_for_company_all(
            company_name=company_name, address=address
        )
        if not check_address:
            await add_new_address(company_name=company_name, address=address)
            await message.reply("Адрес успешно добавлен.")
        elif check_address == 3:
            await message.reply(
                "Данный адрес неактивен для данной компании, пожалуйста, "
                "измените статус адреса на активный командой:\n/return_address",
                reply_markup=ReplyKeyboardRemove(),
            )
        else:
            await message.reply(
                f"Данный адрес для данной компании {company_name}, уже существует."
            )
        await state.clear()
    else:
        await message.reply(f'Ваш сообщение состоит из {len(address)} знаков, пожалуйста этого явно мало для '
                            f'адреса компании. Пожалуйста, введите полный адрес компании')