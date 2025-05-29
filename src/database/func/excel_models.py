import datetime
from typing import Optional

from dateutil.relativedelta import relativedelta
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from src.database.create_db import get_db_session
from src.database.models import Jobs, Staff


async def get_all_data_for_excel(
    time: Optional[int] = None, done: bool = False, all_: bool = False
):
    """
    Функция, возвращающая данные по заявкам по всем сотрудникам для отчета excel
    :return:
    """
    conditions = []
    query = (
        select(Jobs)
        .join(Jobs.company)
        .join(Jobs.address)
        .options(
            joinedload(Jobs.staff),
            joinedload(Jobs.type),
            joinedload(Jobs.company),
            joinedload(Jobs.address),
        )
    )
    if not all_:
        if done:
            conditions.append(Jobs.time_close.is_not(None))
        else:
            conditions.append(Jobs.time_close.is_(None))
    if time:
        now = datetime.datetime.now()
        if time == 1:
            start_data = now - datetime.timedelta(days=1)
        elif time == 7:
            start_data = now - datetime.timedelta(weeks=1)
        elif time == 30:
            start_data = now - relativedelta(months=1)
        conditions.append(Jobs.time_add.between(start_data, now))
    if conditions:
        query = query.where(*conditions)
    async with get_db_session() as session:
        all_data = await session.execute(query)
    return all_data.scalars().all()


async def get_personal_data_for_excel(
    name: str,
    surname: str,
    time: Optional[int] = None,
    done: bool = False,
    all_: bool = False,
) -> list:
    """
    Функция, возвращающая данные по заявкам определенному сотруднику для отчета excel
    :return:
    """
    conditions = [
        Staff.name == name,
        Staff.surname == surname,
    ]
    query = (
        select(Jobs)
        .join(Jobs.staff)
        .join(Jobs.address)
        .options(
            joinedload(Jobs.type),
            joinedload(Jobs.staff),
            joinedload(Jobs.company),
            joinedload(Jobs.address),
        )
    )
    if not all_:
        if done:
            conditions.append(Jobs.time_close.is_not(None))
        else:
            conditions.append(Jobs.time_close.is_(None))
    if time:
        now = datetime.datetime.now()
        if time == 1:
            start_data = now - datetime.timedelta(days=1)
        elif time == 7:
            start_data = now - datetime.timedelta(weeks=1)
        elif time == 30:
            start_data = now - relativedelta(months=1)
        conditions.append(Jobs.time_add.between(start_data, now))

    if conditions:
        query = query.where(*conditions)
    async with get_db_session() as session:
        all_data = await session.execute(query)
    return all_data.scalars().all()
