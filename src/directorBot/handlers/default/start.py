from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config.config import DEFAULT_DIRECTOR_COMMANDS

router_start_dir = Router()


@router_start_dir.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    commands = "\n".join(
        [
            f"/{command[0]} - {command[1]}"
            for command in DEFAULT_DIRECTOR_COMMANDS
        ]
    )
    await message.reply(
        f"Бот для контроля работы сотрудников\n" f"{commands}",
        reply_markup=ReplyKeyboardRemove(),
    )
