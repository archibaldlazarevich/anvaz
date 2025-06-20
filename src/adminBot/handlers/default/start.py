from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config.config import DEFAULT_ADMIN_COMMANDS

router_start_admin = Router()


@router_start_admin.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    commands = "\n".join(
        [f"/{command[0]} - {command[1]}" for command in DEFAULT_ADMIN_COMMANDS]
    )
    await message.answer(
        "Бот для админа.\n"
        "Команды, которые выполняет данный бот:\n"
        f"{commands}",
        reply_markup=ReplyKeyboardRemove(),
    )
