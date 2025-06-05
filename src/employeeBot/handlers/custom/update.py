from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from config.config import ECHO_BOT
from src.database.func.data_func import (
    get_all_dir_id_for_echo,
    get_task_all_data,
    add_change_job,
)
import src.employeeBot.keyboards.reply as rep

# from src.database.func.email_func import send_email

router_update_task = Router()

bot = Bot(token=ECHO_BOT)


class UpdateTask(StatesGroup):
    init: State = State()
    company: State = State()
    address: State = State()
    job_type: State = State()


async def send_job(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    await message.reply(
        "Выберите заявку, которую требуется отредактировать:",
        reply_markup=repl_data[1],
    )


async def send_org(message: Message, state: FSMContext):
    repl_data = await state.get_value("company")
    await message.reply(
        "Выберите организацию из списка:",
        reply_markup=repl_data[1],
    )


async def send_address(message: Message, state: FSMContext):
    repl_data = await state.get_value("address")
    await message.reply("Выберите адрес из списка:", reply_markup=repl_data[1])


async def send_task(message: Message, state: FSMContext):
    repl_data = await state.get_value("job_type")
    await message.reply(
        "Выберите вид работы из списка:", reply_markup=repl_data[1]
    )


async def cancel_func(message: Message, state: FSMContext):
    init_task_data = await state.get_value("init")
    new_company = await state.get_value("company")
    new_address = await state.get_value("address")
    new_job = await state.get_value("job_type")
    task_data = await add_change_job(
        old_data=init_task_data,
        new_company=new_company,
        new_address=new_address,
        new_job=new_job,
        empl_id=message.from_user.id,
    )
    await state.clear()
    await message.reply(
        "Завка успешно изменена:\n"
        f"Номер заяки:{task_data[0]}\n"
        f"Тип работы: {task_data[1][1].capitalize()}\n"
        f"Заказчик: {task_data[2][1].capitalize()}\n"
        f"Адрес объекта: {task_data[3][1].capitalize()}",
        reply_markup=ReplyKeyboardRemove(),
    )
    text = (
        f"Сотрудник {task_data[5][1].title()} {task_data[5][0].title()} изменил старую заявку:\n"
        f"Номер заявки: {task_data[0]}\n"
        f"Тип работы: {task_data[1][0].capitalize()}\n"
        f"Заказчик до изменения: {task_data[2][0].capitalize()}\n"
        f"Адрес до изменения: {task_data[3][0].capitalize()}\n"
        f"Время регистрации первоначальной заявки {task_data[4][0]}\n\n"
        f"На новые данные:\n"
        f"Номер заявки: {task_data[0]}\n"
        f"Тип работы: {task_data[1][1].capitalize()}\n"
        f"Заказчик после изменения: {task_data[2][1].capitalize()}\n"
        f"Адрес после изменения: {task_data[3][1].capitalize()}\n"
        f"Время регистрации последнего изменения заявки {task_data[4][1]}"
    )
    dir_all_id = await get_all_dir_id_for_echo()
    for dir_id in dir_all_id:
        await bot.send_message(
            text=text,
            chat_id=dir_id,
        )


@router_update_task.message(Command("update"))
async def update_task_init(message: Message, state: FSMContext):
    await state.clear()
    repl_data = await rep.check_task(empl_id=message.from_user.id)
    if repl_data:
        await state.set_state(UpdateTask.init)
        await state.update_data(init=repl_data)
        await send_job(message=message, state=state)
    else:
        await message.reply(
            "У вас нет активных заявок.", reply_markup=ReplyKeyboardRemove()
        )


@router_update_task.message(UpdateTask.init)
async def update_company(message: Message, state: FSMContext):
    task_data = await state.get_value("init")
    if message.text in task_data[0]:
        repl_data = await rep.get_company_name_mark()
        if repl_data:
            task_id = int(message.text.split()[2])
            task_all_data = await get_task_all_data(task_id=task_id)
            await message.reply(
                f"Заказчик:\n{task_all_data["company_data"]['name']}",
            )
            await state.update_data(init=task_all_data)
            await state.set_state(UpdateTask.company)
            await state.update_data(company=repl_data)
            await send_org(message=message, state=state)
        else:
            await message.reply(
                "В базе данных нет доступных организаций, сообщите об этом руководителю.",
                reply_markup=ReplyKeyboardRemove(),
            )
            await state.clear()
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_job(message=message, state=state)


@router_update_task.message(UpdateTask.company)
async def change_company(message: Message, state: FSMContext):
    company_data = await state.get_value("company")
    if message.text in company_data[0]:
        company_name = message.text.lower()
        repl_data = await rep.check_address(company_name=company_name)
        if repl_data:
            init_task_data = await state.get_value("init")
            await message.reply(
                f"Адрес объекта:\n{init_task_data["address_data"]["name"]}",
            )
            await state.update_data(company=company_name)
            await state.set_state(UpdateTask.address)
            await state.update_data(address=repl_data)
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


@router_update_task.message(UpdateTask.address)
async def change_address(message: Message, state: FSMContext):
    address_data = await state.get_value("address")
    if message.text in address_data[0]:
        reply_data = await rep.get_all_job_type_reply()
        if reply_data:
            init_task_data = await state.get_value("init")
            await message.reply(
                f"Вид работ:\n{init_task_data["type_data"]["name"]}",
            )
            await state.update_data(address=message.text.lower())
            await state.set_state(UpdateTask.job_type)
            await state.update_data(job_type=reply_data)
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


@router_update_task.message(UpdateTask.job_type)
async def cancel_change(message: Message, state: FSMContext):
    job_type_data = await state.get_value("job_type")
    if message.text in job_type_data[0]:
        await state.update_data(job_type=message.text.lower())
        await cancel_func(message=message, state=state)
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_task(message=message, state=state)
