import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from src.database.func.data_func import get_all_dir_id
from src.directorBot.handlers.custom.change_empl import router_change
from src.directorBot.handlers.default.start import router_start_dir
from src.directorBot.handlers.default.help import router_help_dir
from src.directorBot.handlers.custom.in_process import router_in_process
from src.directorBot.handlers.custom.employee import router_dir_emp

# from src.directorBot.handlers.custom.pdf import router_dir_pdf
from src.directorBot.handlers.custom.excel import router_dir_excel
from src.directorBot.handlers.custom.update_cancel import router_update
from src.directorBot.handlers.custom.busy import router_dir_busy_emp

from src.directorBot.middlewares.middlewares import DirectorAccessMiddleware

from config.config import DIRECTOR_BOT, DEFAULT_DIRECTOR_COMMANDS


bot = Bot(
    token=DIRECTOR_BOT,
)
dp = Dispatcher()


async def set_commands():
    commands = [
        BotCommand(command=command[0], description=command[1])
        for command in DEFAULT_DIRECTOR_COMMANDS
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands()


async def main():
    dp.include_routers(
        router_help_dir,
        router_start_dir,
        router_in_process,
        router_update,
        router_dir_busy_emp,
        # router_dir_pdf,
        router_dir_emp,
        router_dir_excel,
        router_change,
    )
    dp.startup.register(start_bot)
    dp.message.middleware(
        DirectorAccessMiddleware(get_allowed_ids=get_all_dir_id)
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
