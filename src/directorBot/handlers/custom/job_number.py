from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.func.data_func import (
    get_job_number,
)
import src.directorBot.keyboards.reply as rep

router_dir_job_number = Router()


class NumbJob(StatesGroup):
    init: State = State()


async def send_company(message: Message, state: FSMContext):
    """
    Функция отправляет клавиатуру для выбора компании
    :param message:
    :param state:
    :return:
    """
    repl_data = await state.get_value("init")
    await message.reply(
        "Выберите компанию из списка:",
        reply_markup=repl_data[1],
    )


@router_dir_job_number.message(Command("job_number"))
async def job_number(message: Message, state: FSMContext):
    await state.clear()
    repl_result = await rep.get_company_name()
    if repl_result:
        await state.set_state(NumbJob.init)
        await state.update_data(init=repl_result)
        await send_company(message=message, state=state)
    else:
        await message.reply(
            "В данный момент нет доступных компаний.",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_dir_job_number.message(NumbJob.init)
async def send_job_number(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    if message.text in repl_data[0]:
        task_number = await get_job_number(company_name=message.text.lower())
        await state.clear()
        await message.reply(
            f"Количество обработанных заявок для {message.text} всего составляет: {task_number} шт."
        )
    else:
        await message.reply(
            "Пожалуйста, выберите данные из списка!!!",
            reply_markup=ReplyKeyboardRemove(),
        )
        await send_company(message=message, state=state)
