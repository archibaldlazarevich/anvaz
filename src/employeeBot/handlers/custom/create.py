from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from config.config import ECHO_BOT
from src.database.func.data_func import (
    get_all_dir_id_for_echo,
    add_new_job,
)
from src.database.func.email_func import send_email
import src.employeeBot.keyboards.reply as rep

router_create_task = Router()

bot = Bot(token=ECHO_BOT)


class CreateTask(StatesGroup):
    create_task: State = State()
    create_org: State = State()
    create_address: State = State()


async def send_org(message: Message, state: FSMContext):
    repl_data = await state.get_value("create_org")
    await message.reply(
        "Выберите организаию из списка:",
        reply_markup=repl_data[1],
    )


async def send_address(message: Message, state: FSMContext):
    repl_data = await state.get_value("create_address")
    await message.reply("Выберите адрес из списка:", reply_markup=repl_data[1])


async def send_task(message: Message, state: FSMContext):
    repl_data = await state.get_value("create_task")
    await message.reply(
        "Выберите вид работы из списка:", reply_markup=repl_data[1]
    )


async def cancel_func(message: Message, state: FSMContext):
    address_data = await state.get_value("create_address")
    task_data = await state.get_value("create_task")
    company_name = await state.get_value("create_org")
    task_data = await add_new_job(
        empl_id=message.from_user.id,
        address_name=address_data,
        job_name=task_data,
        company_name=company_name,
    )
    await message.reply(
        "Заявка успешно добавлена:\n"
        f"Номер заяки: {task_data[0]}\n"
        f"Заказчик: {task_data[1].capitalize()}\n"
        f"Адрес объекта: {task_data[2].capitalize()}",
        reply_markup=ReplyKeyboardRemove(),
    )
    text = (
        f"Сотрудник {task_data[4].title()} {task_data[3].title()} создал новую заявку:\n"
        f"Номер заявки: {task_data[0]}\n"
        f"Заказчик: {task_data[1].capitalize()}\n"
        f"Адрес объекта: {task_data[2].capitalize()}"
    )
    dir_all_id = await get_all_dir_id_for_echo()
    for dir_id in dir_all_id:
        await bot.send_message(
            text=text,
            chat_id=dir_id,
        )
    await send_email(
        subject=f"Новая заявка от сотрудника {task_data[4].title()} {task_data[3].title()}",
        message=text,
    )
    await state.clear()


@router_create_task.message(Command("create"))
async def create_init(message: Message, state: FSMContext):
    await state.clear()
    repl_data = await rep.get_company_name_mark()
    if repl_data:
        await state.set_state(CreateTask.create_org)
        await state.update_data(create_org=repl_data)
        await send_org(message=message, state=state)
    else:
        await message.reply(
            "В базе данных нет доступных организаций, сообщите об этом руководителю.",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_create_task.message(CreateTask.create_org)
async def create_address_func(message: Message, state: FSMContext):
    org_data = await state.get_value("create_org")
    if message.text in org_data[0]:
        company_data = message.text.lower()
        repl_data = await rep.check_address(company_name=company_data)
        if repl_data:
            await state.update_data(create_org=company_data)
            await state.set_state(CreateTask.create_address)
            await state.update_data(create_address=repl_data)
            await send_address(message=message, state=state)
        else:
            await message.reply(
                "У данной организации нет действующих объектов, сообщите об этом руководителю.",
                reply_markup=ReplyKeyboardRemove(),
            )
            await state.clear()
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_org(message=message, state=state)


@router_create_task.message(CreateTask.create_address)
async def create_task(message: Message, state: FSMContext):
    repl_data = await state.get_value("create_address")
    if message.text in repl_data[0]:
        reply_data = rep.get_all_job_type_reply()
        if reply_data:
            await state.update_data(create_address=message.text.lower())
            await state.set_state(CreateTask.create_task)
            await state.update_data(create_task=reply_data)
            await send_task(message=message, state=state)
        else:
            await message.reply(
                "В данный момент список доступных видов работ пуст, сообщите об этом руководителю",
                reply_markup=ReplyKeyboardRemove(),
            )
            await state.clear()
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_address(message=message, state=state)


@router_create_task.message(CreateTask.create_task)
async def answer_to_user(message: Message, state: FSMContext):
    repl_data = await state.get_value("create_task")
    if message.text in repl_data[0]:
        await state.update_data(create_task=message.text.lower())
        await cancel_func(message=message, state=state)
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_task(message=message, state=state)
