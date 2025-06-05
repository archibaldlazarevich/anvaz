from typing import Optional

from dateutil.relativedelta import relativedelta

from sqlalchemy.orm import joinedload, aliased, contains_eager
import datetime
from sqlalchemy import func, case, desc

from src.database.create_db import get_db_session
from src.database.models import (
    Staff,
    JobType,
    Jobs,
    Company,
    ChangeJobs,
    Address,
)

from sqlalchemy import select, update, and_, insert


async def get_all_data_for_excel(
    name: str = None,
    surname: str = None,
    time: Optional[int] = None,
    done: bool = False,
    all_: bool = False,
):
    """
    Функция, возвращающая данные по заявкам по всем сотрудникам для отчета excel
    :return:
    """
    if name:
        conditions = [
            Staff.name == name,
            Staff.surname == surname,
        ]
    else:
        conditions = []
    query = (
        select(Jobs)
        .join(Jobs.company)
        .join(Jobs.address)
        .join(Jobs.staff)
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
        query = query.where(and_(*conditions))
    async with get_db_session() as session:
        all_data = await session.execute(query)
    return all_data.scalars().all()


async def get_change_data_for_excel(
    name: str = None,
    surname: str = None,
    time: Optional[int] = None,
    done: bool = False,
    all_: bool = False,
) -> list:
    """
    Функция, возвращающая данные по измененным заявкам по определенному сотруднику для отчета excel
    :return:
    """

    company_old = aliased(Company)
    company_new = aliased(Company)
    job_name_old = aliased(JobType)
    job_name_new = aliased(JobType)
    address_old = aliased(Address)
    address_new = aliased(Address)
    if name:
        conditions = [
            Staff.name == name,
            Staff.surname == surname,
        ]
    else:
        conditions = []
    query = (
        select(
            ChangeJobs,
            company_old.company_name.label("old_name"),
            company_new.company_name.label("new_name"),
            job_name_old.job_name.label("job_name_old"),
            job_name_new.job_name.label("job_name_new"),
            address_old.address.label("address_old"),
            address_new.address.label("address_new"),
        )
        .join(ChangeJobs.staff)
        .join(ChangeJobs.jobs)
        .join(company_old, ChangeJobs.company_old_id == company_old.id)
        .outerjoin(company_new, ChangeJobs.company_new_id == company_new.id)
        .join(job_name_old, ChangeJobs.job_id_old == job_name_old.id)
        .outerjoin(job_name_new, ChangeJobs.job_id_new == job_name_new.id)
        .join(address_old, ChangeJobs.address_old_id == address_old.id)
        .outerjoin(address_new, ChangeJobs.address_new_id == address_new.id)
        .options(
            joinedload(ChangeJobs.staff),
            joinedload(ChangeJobs.jobs),
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
        query = query.where(and_(*conditions))
    async with get_db_session() as session:
        all_data = await session.execute(query)
    row = all_data.all()
    return row
