from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from config.config import DEFAULT_DIRECTOR_COMMANDS
from src.directorBot.middlewares.middlewares import TestMiddleware
from src.database.data_func import get_all_dir

router_start_dir = Router()

router_start_dir.message.outer_middleware(TestMiddleware())


@router_start_dir.message(CommandStart())
async def cmd_start(message: Message) -> None:
    if message.from_user.id in await get_all_dir():

    commands = "\n".join(
        [
            f"/{command[0]} - {command[1]}"
            for command in DEFAULT_DIRECTOR_COMMANDS
        ]
    )
    await message.reply(f"Бот для контроля работы сотрудников\n" f"{commands}")
