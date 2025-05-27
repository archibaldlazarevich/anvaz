import asyncio
import os
from datetime import datetime, timedelta

from src.database.func.email_func import send_email_with_attachment
from src.database.func.exel_func import export_sqlalchemy_to_excel
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def back_up_func():
    """
    Функция для отправки данных по бэкапу на специальную почту
    :return:
    """
    now = datetime.now()
    tomorrow = now + timedelta(days=2)

    is_penultimate_day = tomorrow.day == 1
    if 23 > now.hour > 8:
        await send_email_with_attachment(
            subject="База данных",
            message=f'К письму прикреплена версия базы данных за {now.strftime("%H:%M %d.%m.%Y г.")}',
            attachment_path="base.db",
        )
    if now.hour == 23 and now.weekday() not in (5, 6):
        await export_sqlalchemy_to_excel(
            excel_path="day", time=1, all_=True
        )
        await send_email_with_attachment(
            subject="Отчет за день",
            message=f'К письму прикреплен отчет за {now.strftime("%H:%M %d.%m.%Y г.")}',
            attachment_path="day.xlsx",
        )
        os.remove("day.xlsx")
    if now.hour == 23 and now.weekday() == 4:
        await export_sqlalchemy_to_excel(
            excel_path="week", time=7, all_=True
        )
        await send_email_with_attachment(
            subject="Отчет за неделю",
            message=f"К письму прикреплен отчет за неделю",
            attachment_path="week.xlsx",
        )
        os.remove("week.xlsx")
    if now.hour == 23 and is_penultimate_day:
        await export_sqlalchemy_to_excel(
            excel_path="month", time=30, all_=True
        )
        await send_email_with_attachment(
            subject="Отчет за месяц",
            message=f"К письму прикреплен отчет за месяц",
            attachment_path="month.xlsx",
        )
        os.remove("month.xlsx")


async def send_message():
    await back_up_func()


async def scheduler_start():
    await asyncio.sleep(5)
    scheduler.add_job(send_message, trigger="interval", minutes=1)
    scheduler.start()
    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        scheduler.shutdown(wait=False)
        print("Scheduler stopped")


if __name__ == "__main__":
    try:
        asyncio.run(scheduler_start())
    except KeyboardInterrupt:
        print("Scheduler interrupted by user")
