from aiogram import Bot
from aiogram.types import FSInputFile

from config.config import ECHO_BOT
from src.database.func.data_func import get_all_dir_id_for_echo, get_admin_id

bot = Bot(token=ECHO_BOT)


async def send_excel(
    subject,
    message,
    attachment_path,
):
    file = FSInputFile(path=attachment_path, filename=attachment_path)
    log_file = FSInputFile(path=(f"output.log"), filename=f"output.log")
    text = (
        f"Тема сообщения: \n{subject}\n\n" f"Текст сообщения: \n{message}\n\n"
    )
    if "base" in attachment_path:
        all_admin = await get_admin_id()
        for admin_id in all_admin:
            await bot.send_document(
                document=file, chat_id=admin_id, caption=text
            )
            await bot.send_document(
                document=log_file,
                chat_id=admin_id,
                caption="Логи за последний час",
            )
    else:
        dir_all_id = await get_all_dir_id_for_echo()
        for dir_id in dir_all_id:
            await bot.send_document(
                document=file, chat_id=dir_id, caption=text
            )
