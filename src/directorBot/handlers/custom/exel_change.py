import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile

from src.database.func.exel_func import export_change_task
import src.directorBot.keyboards.reply as rep

router_dir_excel_change = Router()

all_data = ["Все сотрудники", "Определённый сотрудник"]


class ExcelChange(StatesGroup):
    init: State = State()
    empl: State = State()
    task: State = State()
    period: State = State()


async def send_spec_empl(message: Message, state: FSMContext):
    """
    Функция отправляет клавиатуру с выбором определенного сотрудника
    :param message:
    :param state:
    :return:
    """
    repl_data = await state.get_value("empl")
    await message.reply(
        "Выберите работника из списка:",
        reply_markup=repl_data[1],
    )


async def send_type(message: Message, state: FSMContext):
    """
    Функция отправляет клавиатуру с выбором типа заявки
    :param message:
    :param state:
    :return:
    """
    repl_data = await state.get_value("task")
    await message.reply("Выберите тип заявки:", reply_markup=repl_data[1])


async def send_period(message: Message, state: FSMContext):
    """
    Функция отправляет клавиатуру с выбором периода дял отчета
    :param message:
    :param state:
    :return:
    """
    repl_data = await state.get_value("period")
    await message.reply(
        "Выбрите период, для которого требуется отчет:",
        reply_markup=repl_data[1],
    )


async def start_command(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ExcelChange.init)
    await message.reply(
        "Выберите необходимый пункт меню:", reply_markup=rep.employee
    )


@router_dir_excel_change.message(Command("excel_change"))
async def busy_init(message: Message, state: FSMContext):
    await start_command(message=message, state=state)


@router_dir_excel_change.message(F.text.not_in(all_data), ExcelChange.init)
async def check(message: Message, state: FSMContext):
    await message.reply(
        "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
    )
    await start_command(message=message, state=state)


@router_dir_excel_change.message(F.text == "Все сотрудники", ExcelChange.init)
async def busy_next(message: Message, state: FSMContext):
    await state.update_data(init=message.text)
    await state.set_state(ExcelChange.task)
    repl_data = await rep.task_choice()
    await state.update_data(task=repl_data)
    await send_type(message=message, state=state)


@router_dir_excel_change.message(
    F.text == "Определённый сотрудник", ExcelChange.init
)
async def busy_person(message: Message, state: FSMContext):
    await state.update_data(init=message.text)
    await state.set_state(ExcelChange.empl)
    repl_data = await rep.get_all_empl_with_change()
    if repl_data:
        await state.update_data(empl=repl_data)
        await send_spec_empl(message=message, state=state)
    else:
        await message.reply(
            "В данный момент нет сотрудников с измененными заявками",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()


@router_dir_excel_change.message(ExcelChange.empl)
async def busy_person_answer(message: Message, state: FSMContext):
    empl_data = await state.get_value("empl")
    if message.text in empl_data[0]:
        name, surname = message.text.split()
        await state.update_data(empl=(name.lower(), surname.lower()))
        await state.set_state(ExcelChange.task)
        repl_data = await rep.task_choice()
        await state.update_data(task=repl_data)
        await send_type(message=message, state=state)
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_spec_empl(message=message, state=state)


@router_dir_excel_change.message(ExcelChange.task)
async def choice_task(message: Message, state: FSMContext):
    task_data = await state.get_value("task")
    if message.text in task_data[0]:
        await state.update_data(task=message.text)
        await state.set_state(ExcelChange.period)
        repl_data = await rep.time_choice()
        await state.update_data(period=repl_data)
        await send_period(message=message, state=state)
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_type(message=message, state=state)


@router_dir_excel_change.message(ExcelChange.period)
async def choice_period(message: Message, state: FSMContext):
    period_data = await state.get_value("period")
    if message.text in period_data[0]:
        state_data = await state.update_data(period=message.text)
        await state.clear()
        await answer(message=message, data=state_data)
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_period(message=message, state=state)


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
        await export_change_task(
            name=name.lower(),
            surname=surname.lower(),
            excel_path=f"{message.from_user.id}",
            **all_data,
        )
        answer = f"{answer_data['tasks']}_{answer_data['time']}_{answer_data['empl'][0].title()}_{answer_data['empl'][1].title()}"
    else:
        await export_change_task(
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
