from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.adminBot.middlewares.middlewares import TestMiddleware
from src.database.data_func import add_job

router_add_jobs = Router()

router_add_jobs.message.outer_middleware(TestMiddleware())


class AddJob(StatesGroup):
    init = State()


@router_add_jobs.message(Command("add_jobs"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.set_state(AddJob.init)
    await message.reply("Напишите наименование работы")


@router_add_jobs.message(AddJob.init)
async def add_dir_choice(message: Message, state: FSMContext):
    await state.clear()
    await add_job(job_name=message.text)
    await message.reply(
        f'Новый тип работы "{message.text}" добавлен в базу данных'
    )
