from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from config.config import EMPLOYEE_BOT
from src.database.func.data_func import (
    check_if_have_busy_amp,
    set_new_empl_for_job,
    get_busy_empl_without_spec_empl,
    get_job_by_id,
)
import src.directorBot.keyboards.reply as rep
from src.database.func.email_func import send_email

router_change = Router()

bot = Bot(token=EMPLOYEE_BOT)


class ChangeEmpl(StatesGroup):
    init: State = State()
    change_empl: State = State()
    update: State = State()


@router_change.message(Command("change"))
async def change_empl_init(message: Message, state: FSMContext):
    result = await check_if_have_busy_amp()
    if result:
        await state.set_state(ChangeEmpl.init)
        await message.reply(
            "Выберите работника из списка:",
            reply_markup=await rep.key_busy_employee(),
        )
    else:
        await message.reply("В данный момент все работники свободны")


@router_change.message(ChangeEmpl.init)
async def change_job_init(message: Message, state: FSMContext):
    name, surname = message.text.split()
    if await get_busy_empl_without_spec_empl(
        name=name.lower(), surname=surname.lower()
    ):
        await state.update_data(init=(name.lower(), surname.lower()))
        await state.set_state(ChangeEmpl.change_empl)
        await message.reply(
            f"Выберите заявку {name} {surname},\nкоторую вы хотите переместить на другого работника:",
            reply_markup=await rep.get_job_by_empl_name(
                name=name.lower(), surname=surname.lower()
            ),
        )
    else:
        await message.reply(
            "В данный момент нет других работников в базе данных"
        )


@router_change.message(ChangeEmpl.change_empl)
async def new_empl(message: Message, state: FSMContext):
    task_id = int(message.text.split()[2])
    state_data = await state.get_data()
    await state.set_state(ChangeEmpl.update)
    name, surname = state_data["init"]
    await state.update_data(update=task_id)
    await message.reply(
        "Выберите работника, которому вы хотите поручить заявку из списка:",
        reply_markup=await rep.key_busy_employee_without_spec(
            name=name.lower(), surname=surname.lower()
        ),
    )


@router_change.message(ChangeEmpl.update)
async def cancel_update(message: Message, state: FSMContext):
    state_data = await state.get_data()
    name, surname = message.text.split()
    task_id = state_data["update"]
    await set_new_empl_for_job(
        task_id=task_id, name=name.lower(), surname=surname.lower()
    )
    new_task_data = await get_job_by_id(task_id=task_id)
    text = (
        "Заявка успешно изменена, новые данные:\n"
        f"Заявка № {new_task_data[0]}\n"
        f"Тип работы: {new_task_data[1].capitalize()}\n"
        f"Организация: {new_task_data[2].capitalize()}\n"
        f"Время поступления заявки: {new_task_data[3]}\n"
        f"Ответсвенный работник: {new_task_data[5].capitalize()} {new_task_data[6].capitalize()}"
    )
    await message.reply(text=text, reply_markup=ReplyKeyboardRemove())
    await bot.send_message(
        text=text,
        chat_id=new_task_data[4],
    )
    await send_email(
        subject=f"Сотрудник {new_task_data[5].capitalize()} {new_task_data[6].capitalize()} переназначен ответсвенным за заявку № {new_task_data[0]}",
        message=text,
    )
