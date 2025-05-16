import asyncio
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
    await send_email_with_attachment(
        subject="База данных",
        message=f'К письму прикреплена версия базы данных за {now.strftime("%H:%M %d.%m.%Y г.")}',
        attachment_path="base.db",
    )
    if now.hour == 23 and now.weekday() not in (5, 6) :
        await export_sqlalchemy_to_excel(excel_path="day_report", time=1)
        await send_email_with_attachment(
            subject="Отчет за день",
            message=f'К письму прикреплен отчет за {now.strftime("%H:%M %d.%m.%Y г.")}',
            attachment_path="day_report.xlsx",
        )
    if now.hour == 23 and now.weekday() == 4:
        await export_sqlalchemy_to_excel(excel_path="week_report", time=7)
        await send_email_with_attachment(
            subject="Отчет за неделю",
            message=f'К письму прикреплен отчет за неделю',
            attachment_path="week_report.xlsx",
        )
    if now.hour == 23 and is_penultimate_day:
        await export_sqlalchemy_to_excel(excel_path="month_report", time=30)
        await send_email_with_attachment(
            subject="Отчет за месяц",
            message=f'К письму прикреплен отчет за месяц',
            attachment_path="month_report.xlsx",
        )


async def send_message():
    await back_up_func()

async def scheduler_start():
    await asyncio.sleep(5)
    scheduler.add_job(
        send_message, trigger="interval", hours=1
    )
    scheduler.start()
    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(scheduler_start())