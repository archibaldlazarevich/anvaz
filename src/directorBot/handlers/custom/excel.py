import asyncio
import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile

from src.database.func.exel_func import export_sqlalchemy_to_excel
import src.directorBot.keyboards.reply as rep

router_dir_excel = Router()


class Excel(StatesGroup):
    init: State = State()
    empl: State = State()
    task: State = State()
    period: State = State()


@router_dir_excel.message(Command("excel"))
async def busy_init(message: Message, state: FSMContext):
    await state.set_state(Excel.init)
    await message.reply(
        "Выберите необходимый пункт меню", reply_markup=rep.employee
    )


@router_dir_excel.message(F.text == "Все сотрудники", Excel.init)
async def busy_next(message: Message, state: FSMContext):
    await state.update_data(init=message.text)
    await state.set_state(Excel.task)
    await message.reply("Выберите тип заявки", reply_markup=rep.task_choice)


@router_dir_excel.message(F.text == "Определённый сотрудник", Excel.init)
async def busy_person(message: Message, state: FSMContext):
    await state.update_data(init=message.text)
    await state.set_state(Excel.empl)
    await message.reply(
        "Выберите работника из списка:",
        reply_markup=await rep.get_all_empl(),
    )


@router_dir_excel.message(Excel.empl)
async def busy_person_answer(message: Message, state: FSMContext):
    name, surname = message.text.split()
    await state.update_data(empl=(name.lower(), surname.lower()))
    await state.set_state(Excel.task)
    await message.reply("Выберите тип заявки", reply_markup=rep.task_choice)


@router_dir_excel.message(Excel.task)
async def choice_task(message: Message, state: FSMContext):
    await state.update_data(task=message.text)
    await state.set_state(Excel.period)
    await message.reply(
        "Выбрите период, для которого составить отчет",
        reply_markup=rep.time_choice,
    )


@router_dir_excel.message(Excel.period)
async def choice_period(message: Message, state: FSMContext):
    state_data = await state.update_data(period=message.text)
    await state.clear()
    await answer(message=message, data=state_data)


async def answer(message: Message, data: dict):
    all_data = {}
    init = data["init"]
    task = data["task"]
    answer_data = {}
    if task == "Все заявки":
        all_data["all_"] = True
        answer_data["tasks"] = "Все_заявки"
    elif task == "Активные заявки":
        all_data["done"] = False
        answer_data["tasks"] = "Активные_заявки"
    elif task == "Завершенные заявки":
        all_data["done"] = True
        answer_data["tasks"] = "Завершенные_заявки"
    period = data["period"]
    answer_data["time"] = "За_все_время"
    if period == "За сутки":
        all_data["time"] = 1
        answer_data["time"] = "За_сутки"
    elif period == "За неделю":
        all_data["time"] = 7
        answer_data["time"] = "За_неделю"
    elif period == "За месяц":
        all_data["time"] = 30
        answer_data["time"] = "За_месяц"
    if init == "Определённый сотрудник":
        empl = data["empl"]
        name = empl[0]
        surname = empl[1]
        answer_data["empl"] = (name, surname)
        await export_sqlalchemy_to_excel(
            name=name.lower(),
            surname=surname.lower(),
            excel_path=f"{message.from_user.id}",
            **all_data,
        )
        answer = f"{answer_data['tasks']}_{answer_data['time']}_{answer_data['empl'][0].title()}_{answer_data['empl'][1].title()}"
    else:
        await export_sqlalchemy_to_excel(
            excel_path=f"{message.from_user.id}", **all_data
        )
        answer = f"{answer_data['tasks']}_{answer_data['time']}_Все_сотрудники"
    file = FSInputFile(
        path=(f"{message.from_user.id}.xlsx"), filename=f"{answer}.xlsx"
    )
    await message.reply_document(
        reply_markup=ReplyKeyboardRemove(), document=file
    )
    os.remove(f"{message.from_user.id}.xlsx")
