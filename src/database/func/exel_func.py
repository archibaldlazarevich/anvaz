import datetime
from typing import Optional

import pandas as pd
from src.database.func.excel_models import (
    get_all_data_for_excel,
    get_change_data_for_excel,
)


async def export_sqlalchemy_to_excel(
    excel_path: str,
    name: Optional[str] = None,
    surname: Optional[str] = None,
    time: Optional[int] = None,
    done: bool = False,
    all_: bool = False,
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
        result = await get_all_data_for_excel(
            name=name, surname=surname, time=time, done=done, all_=all_
        )
    else:
        result = await get_all_data_for_excel(time=time, done=done, all_=all_)
    if result:
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
                str(job.id) if job.id else "Нет заявок",
                job.type.job_name.capitalize() or "Нет заявок",
                job.company.company_name.capitalize() or "Нет заявок",
                job.address.address.capitalize() or "Нет заявок",
                job.staff.name.capitalize() or "Нет заявок",
                job.staff.surname.capitalize() or "Нет заявок",
                (
                    job.time_add.strftime("%H:%M %d.%m.%Y г.")
                    if job.time_add
                    else "Нет заявок"
                ),
                (
                    job.time_close.strftime("%H:%M %d.%m.%Y г.")
                    if job.time_close
                    else "-"
                ),
            ]
            for job in result
        ]
    else:
        headers = ["Заявки отсутсвуют"]
        values_ = [""]
    df = pd.DataFrame(values_, columns=headers)
    df.to_excel(f"{excel_path}.xlsx", index=False)


async def export_change_task(
    excel_path: str,
    name: Optional[str] = None,
    surname: Optional[str] = None,
    time: Optional[int] = None,
    done: bool = False,
    all_: bool = False,
):
    """
    Функция для экспорта данных измененных заявок в эксель
    :param excel_path:
    :param name:
    :param surname:
    :param time:
    :param done:
    :param all_:
    :return:
    """
    if name:
        result = await get_change_data_for_excel(
            name=name, surname=surname, time=time, done=done, all_=all_
        )
    else:
        result = await get_change_data_for_excel(
            time=time, done=done, all_=all_
        )

    if result:
        headers = [
            "№ заявки",
            "Фамилия работника",
            "Имя работника",
            "Вид работы до изменения",
            "Заказчик до изменения",
            "Адрес до изменения",
            "Время регистрации первоначальной заявки",
            "Вид работы после изменения",
            "Заказчик после изменения",
            "Адрес после изменения",
            "Время регистрации последнего изменения заявки",
        ]
        values_ = [
            [
                (
                    str(change_job.jobs.id)
                    if change_job.jobs.id
                    else "Нет заявок"
                ),
                change_job.staff.surname.capitalize() or "Нет заявок",
                change_job.staff.name.capitalize() or "Нет заявок",
                job_name_old or "Нет заявок",
                old_name or "Нет заявок",
                address_old or "Нет заявок",
                datetime.datetime.strftime(
                    change_job.time_init, "%H:%M %d.%m.%Y г."
                )
                or "Нет заявок",
                job_name_new or "Нет заявок",
                new_name or "Нет заявок",
                address_new or "Нет заявок",
                datetime.datetime.strftime(
                    change_job.time_change, "%H:%M %d.%m.%Y г."
                )
                or "Нет заявок",
            ]
            for change_job, old_name, new_name, job_name_old, job_name_new, address_old, address_new, in result
        ]
    else:
        headers = ["Заявки отсутсвуют"]
        values_ = [""]
    df = pd.DataFrame(values_, columns=headers)
    df.to_excel(f"{excel_path}.xlsx", index=False)
