from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config.config import DEFAULT_EMPLOYEE_COMMANDS

router_empl_help = Router()


@router_empl_help.message(Command("help"))
async def empl_help_command(message: Message):
    commands = "\n".join(
        [
            f"/{command[0]} - {command[1]}"
            for command in DEFAULT_EMPLOYEE_COMMANDS
        ]
    )
    await message.reply(
        "Бот для сотрудников анваза.\n"
        "Команды, которые выполняет данный бот:\n"
        f"{commands}"
    )
