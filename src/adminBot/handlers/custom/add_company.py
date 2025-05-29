from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.database.func.data_func import check_all_company, add_company

router_add_company = Router()


class AddCompany(StatesGroup):
    init = State()


@router_add_company.message(Command("add_company"))
async def add_company_init(message: Message, state: FSMContext):
    await state.clear()
    await message.reply(
        "Напишите название компании, которую требуется добавить:",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AddCompany.init)


@router_add_company.message(AddCompany.init)
async def check_company_command(message: Message, state: FSMContext):
    company_name = message.text.lower()
    if len(company_name) > 2:
        check_company_data = await check_all_company(company_name=company_name)
        if check_company_data == 3:
            await message.reply(
                "Данная компания уже добавлена в базу данных, "
                "чтобы сделать ее активной, воспользуйтесь командой /return_company.",
                reply_markup=ReplyKeyboardRemove(),
            )
        elif check_company_data:
            await message.reply(
                "Данная компания уже есть базе данных и она активна.",
                reply_markup=ReplyKeyboardRemove(),
            )
        else:
            await add_company(company_name=company_name)
            await message.reply(
                "Кампания успешно добавлена.",
                reply_markup=ReplyKeyboardRemove(),
            )
        await state.clear()
    else:
        await message.reply(
            f"Ваш сообщение состоит из {len(company_name)} знаков, пожалуйста этого явно мало для "
            f"названия компании. Пожалуйста, введите полное название компании"
        )
