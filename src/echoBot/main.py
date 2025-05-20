import asyncio
import logging

from aiogram import Bot, Dispatcher


from config.config import ECHO_BOT


bot = Bot(
    token=ECHO_BOT,
)
dp = Dispatcher()


async def main():
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
