from email.message import EmailMessage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import Optional

from config.config import EMAIL_NAME, EMAIL_PASSWORD, RECIPIENT_EMAIL


async def send_email(
    subject,
    message,
):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_NAME
    msg["To"] = RECIPIENT_EMAIL
    msg.set_content(message)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_NAME, EMAIL_PASSWORD)
        server.send_message(msg)


async def send_email_with_attachment(
    subject,
    message,
    attachment_path=None,
):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_NAME
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as attachment_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(attachment_path)}",
            )
            msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_NAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_NAME, RECIPIENT_EMAIL, msg.as_string())
