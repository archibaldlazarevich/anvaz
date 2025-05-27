from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import src.adminBot.keyboards.reply as rep
from src.database.func.data_func import return_del_job

router_return_job = Router()


class RetJob(StatesGroup):
    init = State()


@router_return_job.message(Command("return_job"))
async def add_dir_init(message: Message, state: FSMContext):
    await state.clear()
    repl_data = await rep.check_job_del()
    if repl_data:
        await state.set_state(RetJob.init)
        await message.reply(
            "Для возврата в статус используемых видов работ, выберите вид работы из списка:",
            reply_markup=repl_data,
        )
    else:
        await message.reply(
            "В данный момент неактивных видов работ нет в базе данных.",
            reply_markup=ReplyKeyboardRemove(),
        )


@router_return_job.message(RetJob.init)
async def add_dir_choice(message: Message, state: FSMContext):
    await state.clear()
    if await return_del_job(job_name=message.text.lower()):
        await message.reply(
            f"Вид работы {message.text.capitalize()} переведен в активные.",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply(
            "Вы ввели несуществующий вид работ, пожалуйста, выберите вид работ из списка.",
            reply_markup=ReplyKeyboardRemove(),
        )
