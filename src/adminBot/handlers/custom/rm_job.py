from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import src.adminBot.keyboards.reply as rep
from src.database.func.data_func import rm_job

router_rm_jobs = Router()


class RmJob(StatesGroup):
    init = State()


@router_rm_jobs.message(Command("rm_job"))
async def add_dir_init(message: Message, state: FSMContext):
    check_job_mark = await rep.check_job()
    if check_job_mark:
        await state.set_state(RmJob.init)
        await message.reply(
            "Для удаления из базы данных, выберите вид работы из списка",
            reply_markup=check_job_mark,
        )
    else:
        await message.reply(
            "В базе данных нет ни одного добавленного вида работ"
        )


@router_rm_jobs.message(RmJob.init)
async def add_dir_choice(message: Message, state: FSMContext):
    await state.clear()
    await rm_job(job_name=message.text.lower())
    await message.reply(
        f'Вид работ: "{message.text.capitalize()}" удален из базы данных, '
        f"старые заявки с удаленным видом работ всё ещё доступны",
        reply_markup=ReplyKeyboardRemove(),
    )
