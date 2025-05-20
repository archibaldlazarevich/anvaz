from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from config.config import ECHO_BOT
from src.database.func.data_func import (
    get_all_job_by_empl,
    get_company_name,
    insert_new_job_change,
    update_company_name,
    get_address_name_update,
    update_address_for_company,
    get_job_type_update,
    update_job_type,
    get_new_job,
    check_company,
    get_all_dir_id_for_echo,
    update_company_for_task,
    check_address_for_company,
    change_task_by_company,
    set_time_change,
)
import src.employeeBot.keyboards.reply as rep
from src.database.func.email_func import send_email

router_update_task = Router()

bot = Bot(token=ECHO_BOT)


class UpdateTask(StatesGroup):
    init: State = State()
    company: State = State()
    new_company: State = State()
    address: State = State()
    new_address: State = State()
    job_type: State = State()
    new_job_type: State = State()


@router_update_task.message(Command("update"))
async def update_task_init(message: Message, state: FSMContext):
    result = await get_all_job_by_empl(empl_id=message.from_user.id)
    if not result:
        await message.reply("У вас нет активных заявок.")
    else:
        await state.set_state(UpdateTask.init)
        await message.reply(
            "Выберите заявку, которую требуется отредактировать:",
            reply_markup=await rep.check_task(empl_id=message.from_user.id),
        )


@router_update_task.message(UpdateTask.init)
async def update_task_choose_par(message: Message, state: FSMContext):
    task_id = int(message.text.split()[2])
    await state.update_data(init=task_id)
    await state.set_state(UpdateTask.company)
    await insert_new_job_change(job_id=task_id)
    company_name = await get_company_name(job_id=task_id)
    await state.update_data(company=company_name)
    await message.reply(
        f"Заказчик: {company_name.capitalize()}",
        reply_markup=rep.company_choose_rep,
    )


@router_update_task.message(F.text == "Изменить заказчика", UpdateTask.company)
async def change_company(message: Message, state: FSMContext):
    await state.set_state(UpdateTask.new_company)
    company_name = await state.get_value("company")
    check_comp_name = await rep.get_company_name_mark_without_spec(
        company_name=company_name
    )
    await change_task_by_company(company_name=company_name)
    if check_comp_name:
        await message.reply(
            "Введите название организации, либо выберите из списка:",
            reply_markup=check_comp_name,
        )
    else:
        await message.reply(
            "Введите название организации:", reply_markup=ReplyKeyboardRemove()
        )


@router_update_task.message(
    F.text == "Оставить старые данные", UpdateTask.company
)
@router_update_task.message(UpdateTask.new_company)
async def change_address(message: Message, state: FSMContext):
    if await state.get_state() == UpdateTask.new_company.state:
        task_id = await state.get_value("init")
        await state.update_data(company=message.text.lower())
        company_data = await check_company(company_name=message.text.lower())
        if company_data:
            await update_company_for_task(
                company_id=company_data.id, task_id=task_id
            )
            await state.update_data(new_company=False)
        else:
            await update_company_name(
                empl_id=message.from_user.id, new_name=message.text.lower()
            )
        check_address_mark = await rep.check_address_for_update(
            company_name=message.text.lower()
        )
    else:
        check_address_mark = await rep.check_address_for_update(
            company_name=await state.get_value("company")
        )
    address = await get_address_name_update(empl_id=message.from_user.id)
    await message.reply(f"Адрес объекта:\n{address.capitalize()}")
    await state.set_state(UpdateTask.new_address)
    if check_address_mark:
        await message.reply(
            "Введите адрес объекта, либо выберите из списка:",
            reply_markup=check_address_mark,
        )
    else:
        await message.reply(
            "Введите адрес объекта:", reply_markup=ReplyKeyboardRemove()
        )


@router_update_task.message(UpdateTask.new_address)
async def change_job_type(message: Message, state: FSMContext):
    company_name = await state.get_value("company")
    if await check_address_for_company(
        address=message.text.lower(), company_name=company_name
    ):
        await update_address_for_company(
            new_address=message.text.lower(), empl_id=message.from_user.id
        )
    else:
        await update_address_for_company(
            new_address=message.text.lower(),
            empl_id=message.from_user.id,
            new_company=True,
        )
    type_job = await get_job_type_update(empl_id=message.from_user.id)
    await message.reply(
        f"Тип работы :\n{type_job.capitalize()}",
        reply_markup=rep.jobs_choose_rep,
    )
    await state.set_state(UpdateTask.job_type)


@router_update_task.message(
    F.text == "Поменять вид работы", UpdateTask.job_type
)
async def choose_new_job_type(message: Message, state: FSMContext):
    await message.reply(
        "Выберите вид выполняемых работ:",
        reply_markup=await rep.get_all_job_type_reply(),
    )
    await state.set_state(UpdateTask.new_job_type)


@router_update_task.message(UpdateTask.new_job_type)
@router_update_task.message(
    F.text == "Оставить старые данные", UpdateTask.job_type
)
async def cancel_change(message: Message, state: FSMContext):
    if await state.get_state() == UpdateTask.new_job_type.state:
        await update_job_type(
            empl_id=message.from_user.id, job_type=message.text.lower()
        )
    else:
        await set_time_change(empl_id=message.from_user.id)
    task_data = await get_new_job(empl_id=message.from_user.id)
    await message.reply(
        "Завка успешно изменена:\n"
        f"Номер заяки:{task_data[0]}\n"
        f"Тип работы: {task_data[1][1].capitalize()}\n"
        f"Заказчик: {task_data[2][1].capitalize()}\n"
        f"Адресс объекта: {task_data[3][1].capitalize()}",
        reply_markup=ReplyKeyboardRemove(),
    )
    text = (
        f"Сотрудник {task_data[5][1].title()} {task_data[5][0].title()} изменил старую заявку:\n"
        f"Номер заявки: {task_data[0]}\n"
        f"Тип работы: {task_data[1][0].capitalize()}\n"
        f"Заказчик до изменения: {task_data[2][0].capitalize()}\n"
        f"Адресс до изменения: {task_data[3][0].capitalize()}\n"
        f"Время регистрации первоначальной заявки {task_data[4][0]}\n\n"
        f"На новые данные:\n"
        f"Номер заявки: {task_data[0]}\n"
        f"Тип работы: {task_data[1][1].capitalize()}\n"
        f"Заказчик после изменения: {task_data[2][1].capitalize()}\n"
        f"Адресс после изменения: {task_data[3][1].capitalize()}\n"
        f"Время регистрации последнего изменения заявки {task_data[4][1]}\n"
    )
    dir_all_id = await get_all_dir_id_for_echo()
    for dir_id in dir_all_id:
        await bot.send_message(
            text=text,
            chat_id=dir_id,
        )
    await send_email(
        subject=f"{task_data[5][1].title()} {task_data[5][0].title()} изменил заявку № {task_data[0]}",
        message=text,
    )
    await state.clear()
