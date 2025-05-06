from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from config.config import DEFAULT_ADMIN_COMMANDS
from src.directorBot.middlewares.middlewares import TestMiddleware
from src.database.data_func import get_admin_id

router_start_admin = Router()

router_start_admin.message.outer_middleware(TestMiddleware())


@router_start_admin.message(CommandStart())
async def cmd_start(message: Message) -> None:
    if message.from_user.id != await get_admin_id():
        await message.answer('Доступ запрещён')
        return
    commands = "\n".join(
        [
            f"/{command[0]} - {command[1]}"
            for command in DEFAULT_ADMIN_COMMANDS
        ]
    )
    await message.reply(
        "Бот для админа контроля работы сотрудников анваза.\n"
        "Команды, которые выполняет данный бот:\n"
        f"{commands}"
    )
