from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.func.data_func import check_if_have_busy_amp, get_job_by_empl
import src.directorBot.keyboards.reply as rep

router_dir_emp = Router()


class DirEmpState(StatesGroup):
    init: State = State()


@router_dir_emp.message(Command("employee"))
async def dir_emp_init(message: Message, state: FSMContext):
    result = await check_if_have_busy_amp()
    if result:
        await state.set_state(DirEmpState.init)
        await message.reply(
            "Выберите работника из списка:",
            reply_markup=await rep.key_busy_employee(),
        )
    else:
        await message.reply("В данный момент все работники свободны")


@router_dir_emp.message(DirEmpState.init)
async def dir_emp_init(message: Message, state: FSMContext):
    await state.clear()
    name, surname = message.text.split()
    job_data = await get_job_by_empl(
        name=name.lower(), surname=surname.lower()
    )
    await message.reply(f"Действующие заявки на балансе {name} {surname}:")
    for job in job_data:
        await message.answer(
            f"Заявка № {job[0]}\n"
            f"Тип работы: {job[1].capitalize()}\n"
            f"Организация: {job[2].capitalize()}\n"
            f"Время поступления заявки: {job[3]}\n",
            reply_markup=ReplyKeyboardRemove(),
        )
