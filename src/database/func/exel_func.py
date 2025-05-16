from typing import Optional

import pandas as pd
from src.database.func.email_models import (
    get_all_data_for_pdf_or_excel,
    get_personal_data_for_pdf_or_excel,
)


async def export_sqlalchemy_to_excel(
    excel_path: str,
    name: Optional[str] = None,
    surname: Optional[str] = None,
    time: Optional[int]= None,
    done: bool = False,
    all_: bool = False
):
    """
    Функция для экспорта данных в эксель
    :param excel_path:
    :param name:
    :param surname:
    :param time:
    :param done:
    :param all_:
    :return:
    """
    if name:
        result = await get_personal_data_for_pdf_or_excel(
            name=name, surname=surname, time=time, done=done, all_=all_
        )
    else:
        result = await get_all_data_for_pdf_or_excel(time=time, done=done, all_=all_)
    headers = [
        "№ заявки",
        "Наименование работ",
        "Заказчик",
        "Адрес объекта",
        "Фамилия работника",
        "Имя работника",
        "Время регистрации",
        "Время выполнения",
    ]
    values_ = [
        [
            str(job.id),
            job.type.job_name or "",
            job.company.company_name or "",
            job.company.address or "",
            job.staff.name or "",
            job.staff.surname or "",
            job.time_add.strftime("%H:%M %d.%m.%Y г.") if job.time_add else "",
            (
                job.time_close.strftime("%H:%M %d.%m.%Y г.")
                if job.time_close
                else "-"
            ),
        ]
        for job in result
    ]

    df = pd.DataFrame(values_, columns=headers)
    df.to_excel(f"{excel_path}.xlsx", index=False)
