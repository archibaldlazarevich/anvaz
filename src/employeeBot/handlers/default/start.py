from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config.config import DEFAULT_EMPLOYEE_COMMANDS


router_empl_start = Router()


@router_empl_start.message(CommandStart())
async def empl_start_command(message: Message, state: FSMContext):
    await state.clear()
    commands = "\n".join(
        [
            f"/{command[0]} - {command[1]}"
            for command in DEFAULT_EMPLOYEE_COMMANDS
        ]
    )
    await message.reply(
        "Бот для сотрудников анваза.\n"
        "Команды, которые выполняет данный бот:\n"
        f"{commands}",
        reply_markup=ReplyKeyboardRemove(),
    )
