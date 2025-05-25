from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from config.config import EMPLOYEE_BOT
from src.database.func.data_func import (
    set_new_empl_for_job,
    get_busy_empl_without_spec_empl,
)
import src.directorBot.keyboards.reply as rep
from src.database.func.email_func import send_email

router_change = Router()

bot = Bot(token=EMPLOYEE_BOT)


class ChangeEmpl(StatesGroup):
    init: State = State()
    change_empl: State = State()
    update: State = State()


async def send_empl(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    await message.reply("Выберите из списка:", reply_markup=repl_data[1])


async def send_job(message: Message, state: FSMContext):
    repl_job = await state.get_value("change_empl")
    name, surname = state.get_value("init")
    await message.reply(
        f"Выберите заявку {name} {surname},\n"
        f"которую вы хотите переместить на другого работника:",
        reply_markup=repl_job[1],
    )


async def change_empl(message: Message, state: FSMContext):
    repl_data = await state.get_value("change_empl")
    await message.reply(
        "Выберите работника, которому вы хотите поручить заявку из списка:",
        reply_markup=repl_data[1],
    )


@router_change.message(Command("change"))
async def change_empl_init(message: Message, state: FSMContext):
    await state.clear()
    repl_data = await rep.key_busy_employee()
    if repl_data:
        await state.set_state(ChangeEmpl.init)
        await state.update_data(init=repl_data)
        await send_empl(message=message, state=state)
    else:
        await message.reply(
            "В данный момент все работники свободны",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_change.message(ChangeEmpl.init)
async def change_job_init(message: Message, state: FSMContext):
    empl_data = await state.get_value("init")
    if message.text in empl_data[0]:
        name, surname = message.text.split()
        if await get_busy_empl_without_spec_empl(
            name=name.lower(), surname=surname.lower()
        ):
            repl_job = await rep.get_job_by_empl_name(
                name=name.lower(), surname=surname.lower()
            )
            if repl_job:
                await state.update_data(init=(name.lower(), surname.lower()))
                await state.set_state(ChangeEmpl.change_empl)
                await state.update_data(change_empl=repl_job)
                await send_job(message=message, state=state)
            else:
                await message.reply("Работник закрыл действующую заявку.")
        else:
            await message.reply(
                "В данный момент нет других работников в базе данных",
                reply_markup=ReplyKeyboardRemove(),
            )
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_empl(message=message, state=state)


@router_change.message(ChangeEmpl.change_empl)
async def new_empl(message: Message, state: FSMContext):
    task_data = await state.get_value("change_empl")
    if message.text in task_data[0]:
        name, surname = await state.get_value("init")
        repl_busy_data = await rep.key_busy_employee_without_spec(
            name=name.lower(), surname=surname.lower()
        )
        await state.update_data(change_empl=repl_busy_data)
        if repl_busy_data:
            await state.set_state(ChangeEmpl.update)
            await state.update_data(update=int(message.text.split()[2]))
            await change_empl(message=message, state=state)
        else:
            await message.reply("В базе данных нет других сотудников.")
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_job(message=message, state=state)


@router_change.message(ChangeEmpl.update)
async def cancel_update(message: Message, state: FSMContext):
    empl_data = await state.get_value("change_empl")
    if message.text in empl_data[0]:
        name, surname = message.text.split()
        task_id = await state.get_value("update")
        new_task_data = await set_new_empl_for_job(
            task_id=task_id, name=name.lower(), surname=surname.lower()
        )
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
            subject=f"Сотрудник {new_task_data[5].capitalize()} {new_task_data[6].capitalize()}"
            f" переназначен ответсвенным за заявку № {new_task_data[0]}",
            message=text,
        )
        await state.clear()
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await change_empl(message=message, state=state)
