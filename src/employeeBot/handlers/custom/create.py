from pyexpat.errors import messages

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from config.config import ECHO_BOT
from src.database.func.data_func import (
    insert_job_type,
    insert_organization,
    create_new_task,
    add_address,
    check_job,
    get_all_dir_id_for_echo,
)
from src.database.func.email_func import send_email
import src.employeeBot.keyboards.reply as rep

router_create_task = Router()

bot = Bot(token=ECHO_BOT)


class CreateTask(StatesGroup):
    create_task: State = State()
    create_org: State = State()
    create_address: State = State()


@router_create_task.message(Command("create"))
async def create_init(message: Message, state: FSMContext):
    await state.set_state(CreateTask.create_org)
    await create_new_task(empl_id=message.from_user.id)
    check_comp_name = await rep.get_company_name_mark()
    if check_comp_name:
        await message.reply(
            "Введите название организации, либо выберите из списка",
            reply_markup=check_comp_name,
        )
    else:
        await message.reply(
            "Введите название организации",
        )


async def process_create_task(
    message: Message, state: FSMContext, create=True
):
    if create:
        await state.set_state(CreateTask.create_task)
        await insert_organization(
            company_name=message.text.lower(), empl_id=message.from_user.id
        )
    await message.reply(
        "Выберите вид выполняемых работ",
        reply_markup=await rep.get_all_job_type_reply(),
    )


@router_create_task.message(CreateTask.create_org)
async def create_task(message: Message, state: FSMContext):
    await process_create_task(message=message, state=state)


@router_create_task.message(CreateTask.create_task)
async def create_address(message: Message, state: FSMContext):
    if await check_job(job_name=message.text.lower()):
        await state.set_state(CreateTask.create_address)
        await insert_job_type(
            job_type=message.text.lower(), empl_id=message.from_user.id
        )
        check_address_mark = await rep.check_address(
            empl_id=message.from_user.id
        )
        if check_address_mark:
            await message.reply(
                "Введите адрес объекта, либо выберите из списка",
                reply_markup=check_address_mark,
            )
        else:
            await message.reply(
                "Введите адрес объекта", reply_markup=ReplyKeyboardRemove()
            )
    else:
        await message.reply("Выберите вид работ из списка!!!")
        await process_create_task(message=message, state=state, create=False)


@router_create_task.message(CreateTask.create_address)
async def answer_to_user(message: Message, state: FSMContext):
    await state.clear()
    task_data = await add_address(
        address=message.text.lower(), empl_id=message.from_user.id
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
