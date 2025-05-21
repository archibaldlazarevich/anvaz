import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from src.database.func.data_func import get_all_empl_id
from src.employeeBot.handlers.default.start import router_empl_start
from src.employeeBot.handlers.default.help import router_empl_help
from src.employeeBot.handlers.custom.close import router_close_task
from src.employeeBot.handlers.custom.update import router_update_task
from src.employeeBot.handlers.custom.check import router_check_task
from src.employeeBot.handlers.custom.create import router_create_task

from src.employeeBot.middlewares.middlewares import EmployeeAccessMiddleware

from config.config import EMPLOYEE_BOT, DEFAULT_EMPLOYEE_COMMANDS


bot = Bot(
    token=EMPLOYEE_BOT,
)
dp = Dispatcher()


async def set_commands():
    commands = [
        BotCommand(command=command[0], description=command[1])
        for command in DEFAULT_EMPLOYEE_COMMANDS
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands()


async def main():
    dp.include_routers(
        router_empl_help,
        router_create_task,
        router_close_task,
        router_update_task,
        router_check_task,
        router_empl_start,
    )
    dp.startup.register(start_bot)
    dp.message.middleware(
        EmployeeAccessMiddleware(get_allowed_ids=get_all_empl_id)
    )
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot, allowed_updates=dp.resolve_used_update_types()
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
