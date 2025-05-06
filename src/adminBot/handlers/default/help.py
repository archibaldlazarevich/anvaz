from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config.config import DEFAULT_ADMIN_COMMANDS

router_help_admin = Router()


@router_help_admin.message(Command("help"))
async def get_help(message: Message):
    commands = "\n".join(
        [
            f"/{command[0]} - {command[1]}"
            for command in DEFAULT_ADMIN_COMMANDS
        ]
    )
    await message.answer(
        "Бот для админа.\n"
        "Команды, которые выполняет данный бот:\n"
        f"{commands}"
    )
