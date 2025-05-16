from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.adminBot.middlewares.middlewares import TestMiddleware
import src.adminBot.keyboards.reply as rep
from src.database.func.data_func import rm_job

router_rm_jobs = Router()

router_rm_jobs.message.outer_middleware(TestMiddleware())


class RmJob(StatesGroup):
    init = State()


@router_rm_jobs.message(Command("rm_job"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.set_state(RmJob.init)
    await message.reply(
        "Для удаления из базы данных, выберите вид работы из списка",
        reply_markup=await rep.check_job(),
    )


@router_rm_jobs.message(RmJob.init)
async def add_dir_choice(message: Message, state: FSMContext):
    await state.clear()
    await rm_job(job_name=message.text)
    await message.reply(
        f'Вид работ: "{message.text}" удален из базы данных, '
        f"старые заявки с удаленным видом работ всё ещё доступны",
        reply_markup=ReplyKeyboardRemove(),
    )
