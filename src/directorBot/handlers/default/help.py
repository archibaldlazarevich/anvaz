from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config.config import DEFAULT_DIRECTOR_COMMANDS
from src.database.data_func import get_all_dir_id

router_help_dir = Router()


@router_help_dir.message(Command("help"))
async def get_help(message: Message):
    commands = "\n".join(
        [
            f"/{command[0]} - {command[1]}"
            for command in DEFAULT_DIRECTOR_COMMANDS
        ]
    )
    await message.answer(
        "Бот для контроля работы сотрудников.\n"
        "Команды, которые выполняет данный бот:\n"
        f"{commands}"
    )
