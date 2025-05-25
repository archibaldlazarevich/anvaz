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


async def send_empl(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    await message.reply("Выберите из списка:", reply_markup=repl_data[1])


@router_dir_emp.message(Command("employee"))
async def dir_emp_init(message: Message, state: FSMContext):
    await state.clear()
    result = await check_if_have_busy_amp()
    if result:
        repl_data = await rep.get_all_empl()
        await state.set_state(DirEmpState.init)
        await state.update_data(init=repl_data)
        await send_empl(message=message, state=state)
    else:
        await message.reply(
            "В данный момент все работники свободны",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_dir_emp.message(DirEmpState.init)
async def dir_emp_init(message: Message, state: FSMContext):
    empl_data = await state.get_value("init")
    if message.text in empl_data[0]:
        await state.clear()
        name, surname = message.text.split()
        job_data = await get_job_by_empl(
            name=name.lower(), surname=surname.lower()
        )
        if job_data:
            await message.reply(
                f"Действующие заявки на балансе {name} {surname}:"
            )
            for job in job_data:
                await message.answer(
                    f"Заявка № {job[0]}\n"
                    f"Тип работы: {job[1].capitalize()}\n"
                    f"Организация: {job[2].capitalize()}\n"
                    f"Время поступления заявки: {job[3]}\n",
                    reply_markup=ReplyKeyboardRemove(),
                )
        else:
            await message.reply(
                f"В данный момент у {name} {surname} нет действующий заявок.",
                reply_markup=ReplyKeyboardRemove(),
            )
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_empl(message=message, state=state)
