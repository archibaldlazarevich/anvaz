from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.database.func.data_func import add_job, check_job

router_add_jobs = Router()


class AddJob(StatesGroup):
    init = State()


@router_add_jobs.message(Command("add_jobs"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddJob.init)
    await message.reply(
        "Напишите наименование работы", reply_markup=ReplyKeyboardRemove()
    )


@router_add_jobs.message(AddJob.init)
async def add_dir_choice(message: Message, state: FSMContext):
    job = message.text
    if len(job) > 4:
        if not await check_job(job_name=job.lower()):
            await state.clear()
            await add_job(job_name=job.lower())
            await message.reply(
                f'Новый тип работы "{message.text}" добавлен в базу данных',
                reply_markup=ReplyKeyboardRemove(),
            )
        else:
            await message.reply(
                "Данный вид работ уже есть в базе данных, "
                "если он неактивен, восстановите его командой:\n/return_job"
            )
    else:
        await message.reply(
            f"Ваш сообщение состоит из {len(job)} знаков, пожалуйста этого явно мало для "
            f"обозначения вида работ. Пожалуйста, введите полное название работ"
        )
