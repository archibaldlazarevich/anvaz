import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from src.registrationBot.handlers.default.start import router_register_start

from config.config import REGISTER_BOT, DEFAULT_REGISTER_COMMAND


bot = Bot(
    token=REGISTER_BOT,
)
dp = Dispatcher()


async def set_commands():
    commands = [
        BotCommand(command=command[0], description=command[1])
        for command in DEFAULT_REGISTER_COMMAND
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands()


async def main():
    dp.include_routers(
        router_register_start,
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
