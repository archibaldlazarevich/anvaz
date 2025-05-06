import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from src.adminBot.handlers.default.start import router_start_admin
from src.adminBot.handlers.default.help import router_help_admin

from src.adminBot.handlers.custom.add_director import router_add_directors
from src.adminBot.handlers.custom.add_employee import router_add_empl
from src.adminBot.handlers.custom.add_jobs import router_add_jobs
from src.adminBot.handlers.custom.directors_list import router_dir_list
from src.adminBot.handlers.custom.employee_list import router_emp_list
from src.adminBot.handlers.custom.jobs_list import router_jobs_list
from src.adminBot.handlers.custom.non_staff_list import router_non_staff_list
from src.adminBot.handlers.custom.number_employee import router_emp_number
from src.adminBot.handlers.custom.rm_director import router_rm_directors
from src.adminBot.handlers.custom.rm_employee import router_rm_employee
from src.adminBot.handlers.custom.rm_job import router_rm_jobs
from src.adminBot.handlers.custom.rm_non_employee import router_rm_non_staff

from config.config import ADMIN_BOT, DEFAULT_ADMIN_COMMANDS


bot = Bot(
    token=ADMIN_BOT,
)
dp = Dispatcher()


async def set_commands():
    commands = [
        BotCommand(command=command[0], description=command[1])
        for command in DEFAULT_ADMIN_COMMANDS
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands()


async def main():
    dp.include_routers(
        router_help_admin,
        router_start_admin,
        router_add_directors,
        router_add_empl,
        router_add_jobs,
        router_dir_list,
        router_emp_list,
        router_jobs_list,
        router_non_staff_list,
        router_emp_number,
        router_rm_directors,
        router_rm_employee,
        router_rm_jobs,
        router_rm_non_staff,
    )
    dp.startup.register(start_bot)
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
