# from email.message import EmailMessage
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
# import os
# import requests
from aiogram import Bot
from aiogram.types import FSInputFile

from config.config import  ECHO_BOT
from src.database.func.data_func import get_all_dir_id_for_echo, get_admin_id

bot = Bot(token=ECHO_BOT)

# async def send_email(
#     subject,
#     message,
# ):
#     # msg = EmailMessage()
#     # msg["Subject"] = subject
#     # msg["From"] = EMAIL_NAME
#     # msg["To"] = RECIPIENT_EMAIL
#     # msg.set_content(message)
#     #
#     # with smtplib.SMTP("smtp.gmail.com", 587) as server:
#     #     server.starttls()
#     #     server.login(EMAIL_NAME, EMAIL_PASSWORD)
#     #     server.send_message(msg)
#
#
#     API_TOKEN = "8b8e117b8128a0b7d3ddad4ec4a83e75"
#     API_URL = "https://api.mailopost.ru/v1/email/messages"
#
#     headers = {
#         "Authorization": f"Bearer {API_TOKEN}",
#         # Content-Type не указываем, requests сам выставит multipart/form-data
#     }
#
#     # Параметры письма
#     data = {
#         "from_email": "pythonnewpart@gmail.com",
#         "from_name": "Ваше имя или компания",
#         "to": "compact_00@mail.ru",
#         "subject": subject,
#         "text": message,
#         "html": "<h1>message</h1>"
#     }
#
#     # Открываем файл в бинарном режиме
#     # with open("путь_к_файлу/файл.pdf", "rb") as f:
#     #     files = {
#     #         "attachments": ("файл.pdf", f, "application/pdf")
#     #     }
#
#     response = requests.post(API_URL,
#                              headers=headers,
#                              json=data,
#                              # files=files
#                              )
#
#     if response.status_code in (200, 201):
#         print("Письмо с вложением успешно отправлено!")
#     else:
#         print(f"Ошибка: {response.status_code}")
#         print(response.text)


async def send_email_with_attachment(
    subject,
    message,
    attachment_path,
):
    # msg = MIMEMultipart()
    # msg["From"] = EMAIL_NAME
    # msg["To"] = RECIPIENT_EMAIL
    # msg["Subject"] = subject
    #
    # msg.attach(MIMEText(message, "plain"))
    #
    # if attachment_path and os.path.exists(attachment_path):
    #     with open(attachment_path, "rb") as attachment_file:
    #         part = MIMEBase("application", "octet-stream")
    #         part.set_payload(attachment_file.read())
    #         encoders.encode_base64(part)
    #         part.add_header(
    #             "Content-Disposition",
    #             f"attachment; filename={os.path.basename(attachment_path)}",
    #         )
    #         msg.attach(part)
    #
    # with smtplib.SMTP("smtp.gmail.com", 587) as server:
    #     server.starttls()
    #     server.login(EMAIL_NAME, EMAIL_PASSWORD)
    #     server.sendmail(EMAIL_NAME, RECIPIENT_EMAIL, msg.as_string())
    file = FSInputFile(
        path=(f"{attachment_path}"), filename=f"{attachment_path}"
    )
    log_file = FSInputFile(
        path=(f"output.log"), filename=f"output.log"
    )
    text = (f'Тема сообщения: \n{subject}\n\n'
            f'Текст сообщения: \n{message}\n\n')
    if 'base' in attachment_path:
        all_admin = await get_admin_id()
        for admin_id in all_admin:
            await bot.send_document(document=file, chat_id=admin_id, caption=text)
            await bot.send_document(document=log_file, chat_id=admin_id, caption='Логи за последний час')
    else:
        dir_all_id = await get_all_dir_id_for_echo()
        for dir_id in dir_all_id:
            await bot.send_document(document=file, chat_id=dir_id, caption=text)
