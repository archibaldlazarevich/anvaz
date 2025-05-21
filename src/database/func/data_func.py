from sqlalchemy.orm import joinedload, aliased
import datetime
from sqlalchemy import func, case, desc

from src.database.create_db import get_db_session
from src.database.models import (
    Staff,
    JobType,
    Admin,
    Jobs,
    Company,
    ChangeJobs,
    Address,
)

from sqlalchemy import select, update, and_, insert, delete


async def add_direct(name: str, surname: str) -> int:
    """
    Функция для изменения статуса пользователя на статус начальника
    :param name: Имя пользователя
    :param surname: Фамилия пользователя
    :return: int статус
    """
    async with get_db_session() as session:
        director_data = await session.execute(
            update(Staff)
            .where(and_(Staff.name == name, Staff.surname == surname))
            .values(status=3)
            .returning(Staff.status)
        )
        await session.commit()
        director = director_data.scalar_one_or_none()
    return director


async def get_all_non_employee() -> list:
    """
    Функция для поиска всех не работников в базе данных
    :return:
    """
    async with get_db_session() as session:
        staff_data = await session.execute(
            select(Staff).where(Staff.status == 1)
        )
        staff_data = staff_data.scalars()
    return [(person.name, person.surname) for person in staff_data]


async def get_all_del_non_employee() -> list:
    """
    Функция для поиска всех неактивных пользвателей
    :return:
    """
    async with get_db_session() as session:
        staff_data = await session.execute(
            select(Staff).where(Staff.status == 4)
        )
        staff_data = staff_data.scalars()
    return [(person.name, person.surname) for person in staff_data]


async def add_employee(name: str, surname: str) -> int:
    """
    Функция для изменения статуса пользователя на статус начальника
    :param name: Имя пользователя
    :param surname: Фамилия пользователя
    :return: int статус
    """
    async with get_db_session() as session:
        emp_data = await session.execute(
            update(Staff)
            .where(and_(Staff.name == name, Staff.surname == surname))
            .values(status=2)
            .returning(Staff.status)
        )
        await session.commit()
        emp = emp_data.scalar_one_or_none()
    return emp


async def add_job(job_name: str) -> None:
    """
    Функция по добавлению нового вида работы в базу
    :return:
    """
    async with get_db_session() as session:
        await session.execute(
            insert(JobType).values(job_name=job_name, active=1)
        )
        await session.commit()


async def get_all_dir() -> list:
    """
    Функция по получению всех директоров в б.д.
    :return:
    """
    async with get_db_session() as session:
        all_dir_data = await session.execute(
            select(Staff).where(Staff.status == 3)
        )
        all_dir_data = all_dir_data.scalars()
    return [(person.name, person.surname) for person in all_dir_data]


async def get_all_emp() -> list:
    """
    Функция по получению всех работников в б.д.
    :return:
    """
    async with get_db_session() as session:
        all_emp_data = await session.execute(
            select(Staff).where(Staff.status == 2)
        )
        all_emp_data = all_emp_data.scalars()
    return [(person.name, person.surname) for person in all_emp_data]


async def get_all_jobs() -> list:
    """
    Функция по получению всех видов работ в б.д.
    :return:
    """
    async with get_db_session() as session:
        all_jobs_data = await session.execute(
            select(JobType).where(JobType.active == 1)
        )
        all_jobs_data = all_jobs_data.scalars()
    return [job.job_name for job in all_jobs_data]


async def get_all_dell_job() -> list:
    """
    Функция по получению всех неактивных видов работ в б.д.
    :return:
    """
    async with get_db_session() as session:
        all_jobs_data = await session.execute(
            select(JobType).where(JobType.active == 0)
        )
        all_jobs_data = all_jobs_data.scalars()
    return [job.job_name for job in all_jobs_data]


async def return_del_job(job_name: str):
    """
    Функция по возвращению вида работ в активные
    :param job_name:
    :return:
    """

    async with get_db_session() as session:
        await session.execute(
            update(JobType)
            .where(JobType.job_name == job_name)
            .values(active=1)
        )
        await session.commit()


async def rm_direct(name: str, surname: str) -> bool:
    """
    Функция для изменения статуса начальника на статус пользователя
    :param name: Имя начальникиа
    :param surname: Фамилия начальника
    :return: int статус
    """
    async with get_db_session() as session:
        director_data = await session.execute(
            update(Staff)
            .where(and_(Staff.name == name, Staff.surname == surname))
            .values(status=1)
            .returning(Staff.status)
        )
        await session.commit()
        director = director_data.scalar_one_or_none()
    return director == 1


async def rm_employee(name: str, surname: str) -> bool:
    """
    Функция для изменения статуса работника на статус пользователя
    :param name: Имя работника
    :param surname: Фамилия работника
    :return: int статус
    """
    async with get_db_session() as session:
        empl_data = await session.execute(
            update(Staff)
            .where(and_(Staff.name == name, Staff.surname == surname))
            .values(status=1)
            .returning(Staff.status)
        )
        await session.commit()
        employee = empl_data.scalar_one_or_none()
    return employee == 1


async def rm_job(job_name: str) -> None:
    """
    Функция для удаления вида работы
    :param job_name: наименование работы
    :return: None
    """
    async with get_db_session() as session:
        await session.execute(
            update(JobType)
            .where(JobType.job_name == job_name)
            .values(active=0)
        )
        await session.commit()


async def rm_non_staff(name: str, surname: str) -> bool:
    """
    Функция для удаления пользователя из списка (статус - 4)
    :param name:
    :param surname:
    :return: None
    """
    async with get_db_session() as session:
        empl_data = await session.execute(
            update(Staff)
            .where(and_(Staff.name == name, Staff.surname == surname))
            .values(status=4)
            .returning(Staff.status)
        )
        await session.commit()
    employee = empl_data.scalar_one_or_none()
    return employee == 4


async def get_all_dell() -> list:
    """
    Функция по получению всех забаненных пользователей
    :return:
    """
    async with get_db_session() as session:
        all_emp_data = await session.execute(
            select(Staff).where(Staff.status == 4)
        )
        all_emp_data = all_emp_data.scalars()
    return [(person.name, person.surname) for person in all_emp_data]


async def return_del(name: str, surname: str) -> bool:
    """
    Функция для изменения статуса пользователя на активный
    :param name: Имя работника
    :param surname: Фамилия работника
    :return: int статус
    """

    async with get_db_session() as session:
        empl_data = await session.execute(
            update(Staff)
            .where(and_(Staff.name == name, Staff.surname == surname))
            .values(status=1)
            .returning(Staff.status)
        )
        await session.commit()
        employee = empl_data.scalar_one_or_none()
    print(employee)
    return employee == 1


async def get_admin_id() -> list[int]:
    """
    Функция для получения id админа
    :return:
    """
    async with get_db_session() as session:
        data_admin = await session.execute(select(Admin))
    return [admin.tel_ad_id for admin in data_admin.scalars()]


async def get_all_dir_id() -> list[int]:
    """
    Функция для получения id начальников в базе данных
    :return:
    """
    async with get_db_session() as session:
        data_dir = await session.execute(
            select(Staff).where(Staff.status == 3)
        )
    return [dir_.tel_id for dir_ in data_dir.scalars()]


async def get_all_dir_id_for_echo() -> list[int]:
    """
    Функция для получения id начальников в базе данных для отправки эъо сообщений
    :return:
    """
    async with get_db_session() as session:
        data_dir = await session.execute(
            select(Staff).where(
                and_(
                    Staff.status == 3,
                    Staff.check_job == 1,
                )
            )
        )
    return [dir_.tel_id for dir_ in data_dir.scalars()]


async def get_all_empl_id() -> list[int]:
    """
    Функция для получения id сотрудников в базе данных
    :return:
    """
    async with get_db_session() as session:
        data_emp = await session.execute(
            select(Staff).where(Staff.status == 2)
        )
    return [emp.tel_id for emp in data_emp.scalars()]


async def get_all_proc_jobs() -> list:
    """
    Функция, возвращающия список действующих заявок
    :return:
    """
    async with get_db_session() as session:
        proc_data = await session.execute(
            select(Jobs)
            .where(Jobs.time_close.is_(None))
            .join(Jobs.staff)
            .join(Jobs.type)
            .join(Jobs.company)
            .options(
                joinedload(Jobs.staff),
                joinedload(Jobs.type),
                joinedload(Jobs.company),
            )
            .group_by(Jobs.id)
            .order_by(Jobs.id)
        )
        procs = proc_data.scalars().all()
    return [
        (
            proc.id,
            proc.type.job_name,
            proc.company.company_name,
            datetime.datetime.strftime(proc.time_add, "%H:%M %d.%m.%Y г."),
            proc.staff.name,
            proc.staff.surname,
        )
        for proc in procs
    ]


async def check_if_update(dir_id: int) -> bool:
    """
    Функция для проверки подписки на обновления заявок
    :param dir_id: id пользователя в телеграм
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            select(Staff).where(
                and_(Staff.tel_id == dir_id, Staff.check_job.isnot(None))
            )
        )
        result_data = result_data.scalar()
    return result_data is not None


async def check_update_sub(dir_id: int) -> None:
    """
    Функция для подписки на обновления
    :param dir_id: id пользователя в телеграмм
    :return:
    """

    async with get_db_session() as session:
        await session.execute(
            update(Staff)
            .where(and_(Staff.tel_id == dir_id, Staff.status == 3))
            .values(check_job=1)
        )
        await session.commit()


async def cancel_update(dir_id: int) -> None:
    """
    Функция для завершения подписки на обновления
    :param dir_id: id пользователя в телеграмм
    :return:
    """
    async with get_db_session() as session:
        await session.execute(
            update(Staff).where(Staff.tel_id == dir_id).values(check_job=None)
        )
        await session.commit()


async def check_if_have_busy_amp() -> bool:
    """
    Функци для проверки наличия занятых работников
    :return:
    """

    async with get_db_session() as session:
        result_data = await session.execute(
            select(func.count(Jobs.id)).where(Jobs.time_close.is_(None))
        )
        result_data = result_data.scalar()
    if result_data >= 1:
        return True
    return False


async def set_new_empl_for_job(task_id: int, name: str, surname: str):
    """
    Функция, которая устанавливает нового работника для заявки
    :param task_id:
    :param name:
    :param surname:
    :return:
    """
    async with get_db_session() as session:
        staff_data = await session.execute(
            select(Staff.id).where(
                and_(Staff.name == name, Staff.surname == surname)
            )
        )
        staff_id = staff_data.scalar_one_or_none()
        await session.execute(
            update(Jobs)
            .where(and_(Jobs.id == task_id))
            .values(employee=staff_id)
        )
        await session.commit()


async def get_busy_empl_without_spec_empl(name: str, surname: str):
    """
    Функция для проверки о наличии работников в базу данных кроме предоставленного
    :param name:
    :param surname:
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            select(Staff).where(
                and_(
                    Staff.status == 2,
                    Staff.name != name,
                    Staff.surname != surname,
                )
            )
        )
        result = result_data.scalars().all()
    return [(staff.name, staff.surname) for staff in result] if result else []


async def get_all_company_name_without_spec(company_name: str):
    """
    Возвращает все компании, кроме переданной
    :param company_name:
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            select(Company.company_name).where(
                Company.company_name != company_name
            )
        )
        result = result_data.scalars().all()
    return [company for company in result] if result else []


async def get_busy_empl() -> list:
    """
    Функция для выбора занятых работников
    :return: list
    """

    async with get_db_session() as session:
        result_data = await session.execute(
            select(Staff)
            .join(Staff.jobs)
            .options(joinedload(Staff.jobs))
            .where(Jobs.time_close.is_(None))
        )
        result_data = result_data.unique().scalars().all()
    return [(staff.name, staff.surname) for staff in result_data]


async def get_job_by_id(task_id: int):
    """
    Функция, возвращающая данные по определенной заявке
    :param task_id:
    :return:
    """
    async with get_db_session() as session:
        proc_data = await session.execute(
            select(Jobs)
            .options(
                joinedload(Jobs.staff),
                joinedload(Jobs.type),
                joinedload(Jobs.company),
            )
            .where(
                and_(
                    Jobs.id == task_id,
                )
            )
            .order_by(Jobs.id)
        )
        proc = proc_data.scalar_one_or_none()
    return [
        proc.id,
        proc.type.job_name,
        proc.company.company_name,
        datetime.datetime.strftime(proc.time_add, "%H:%M %d.%m.%Y г."),
        proc.staff.tel_id,
        proc.staff.name,
        proc.staff.surname,
    ]


async def get_job_by_empl(name: str, surname: str) -> list:
    """
    Функция, возвращающия список действующих заявок для определенного сотрудника
    :return:
    """
    async with get_db_session() as session:
        proc_data = await session.execute(
            select(Jobs)
            .join(Jobs.staff)
            .options(
                joinedload(Jobs.staff),
                joinedload(Jobs.type),
                joinedload(Jobs.company),
            )
            .where(
                and_(
                    Jobs.time_close.is_(None),
                    Staff.name == name,
                    Staff.surname == surname,
                )
            )
            .order_by(Jobs.id)
        )
        procs = proc_data.scalars().all()
    return [
        (
            proc.id,
            proc.type.job_name,
            proc.company.company_name,
            datetime.datetime.strftime(proc.time_add, "%H:%M %d.%m.%Y г."),
        )
        for proc in procs
    ]


async def get_all_busy_empl() -> list:
    """
    Функция возвращающая данные по всем занятым сотрудникам
    :return:
    """
    async with get_db_session() as session:
        proc_data = await session.execute(
            select(
                Jobs,
                func.count(
                    case((Jobs.time_close.is_(None), Jobs.id), else_=None)
                ).label("jobs_count"),
            )
            .join(Jobs.staff)
            .options(
                joinedload(Jobs.staff),
            )
            .where(Jobs.time_close.is_(None))
            .group_by(Staff.id)
            .order_by(Staff.id)
        )
        procs = proc_data.unique().all()
    return [
        (
            job.staff.name,
            job.staff.surname,
            job_count,
        )
        for job, job_count in procs
    ]


async def get_all_job_type() -> list:
    """
    Функция, возвращающая все виды работ из базу данных
    :return:
    """

    async with get_db_session() as session:
        job_type_data = await session.execute(select(JobType))
    return [job_type.job_name for job_type in job_type_data.scalars().all()]


async def insert_job_type(job_type: str, empl_id: int):
    """
    Добавляет в базу данных завку и тип работы
    :return:
    """
    job_id = await get_last_task_by_empl(empl_id=empl_id)
    async with get_db_session() as session:
        job_type_data = await session.execute(
            select(JobType).where(JobType.job_name == job_type)
        )
        job_type_id = job_type_data.scalar_one_or_none().id
        await session.execute(
            update(Jobs).where(Jobs.id == job_id).values(job_id=job_type_id)
        )
        await session.commit()


async def get_all_company_name():
    """
    Функция, возвращающая список названий компаний, которые есть в бд
    :return:
    """
    async with get_db_session() as session:
        company_name_data = await session.execute(select(Company.company_name))
    return [company_name for company_name in company_name_data.scalars()]


async def insert_organization(empl_id: int, company_name: str):
    """
    Функция, дабавляющая в базу даных, обслуживаемаю организацию
    :return:
    """
    job_id = await get_last_task_by_empl(empl_id=empl_id)
    async with get_db_session() as session:
        company_data = await session.execute(
            select(Company).where(Company.company_name == company_name)
        )
        company = company_data.scalar_one_or_none()
        if company is None:
            new_company_data = await session.execute(
                insert(Company)
                .values(company_name=company_name)
                .returning(Company)
            )
            company = new_company_data.scalar_one_or_none()
        await session.execute(
            update(Jobs).where(Jobs.id == job_id).values(company_id=company.id)
        )
        await session.commit()


async def create_new_task(empl_id: int):
    """
    Функция, создающая новую задачу работника
    :param empl_id: id работника
    :return:
    """

    async with get_db_session() as session:
        empl_data = await session.execute(
            select(Staff.id).where(
                and_(
                    Staff.tel_id == empl_id,
                    Staff.status == 2,  #### удалить Правка
                )
            )
        )
        await session.execute(
            insert(Jobs).values(employee=empl_data.scalar_one_or_none())
        )
        await session.commit()


async def get_last_task_by_empl(empl_id: int) -> int:
    """
    Функция, возвращающая id последней добавленной работником задачи
    :param empl_id: id работника
    :return:
    """

    async with get_db_session() as session:
        empl_id_data = await session.execute(
            select(Staff.id).where(
                and_(Staff.tel_id == empl_id, Staff.status == 2)  ### Правка
            )
        )
        task_data = await session.execute(
            select(Jobs.id)
            .where(Jobs.employee == empl_id_data.scalar_one_or_none())
            .order_by(desc(Jobs.id))
            .limit(1)
        )
        task_id = task_data.scalar_one_or_none()
    return task_id


async def get_address_by_empl_id(empl_id: int) -> bool | list:
    """
    Функция, возращающая либо список аддресов объектов компании, либо None при их отсутствии
    :param empl_id:
    :return:
    """
    jobs_data = await get_last_company_by_empl(empl_id=empl_id)
    async with get_db_session() as session:
        addresses_data = await session.execute(
            select(Address.address).where(
                Address.company_id == jobs_data.company.id
            )
        )
        addresses = addresses_data.scalars().all()
    if len(addresses) != 0:
        return addresses
    return False


async def get_last_company_by_empl(empl_id: int):
    """
    Функция, возращающая последнюю работу из последней зарег задачи
    :param empl_id:
    :return:
    """

    async with get_db_session() as session:
        company_id_data = await session.execute(
            select(Jobs)
            .join(Jobs.staff)
            .join(Jobs.company)
            .options(joinedload(Jobs.staff), joinedload(Jobs.company))
            .where(
                and_(
                    Staff.tel_id == empl_id,
                    Staff.status == 2,
                )
            )
            .order_by(desc(Jobs.id))
            .limit(1)
        )
        jobs_data = company_id_data.scalars().one_or_none()
    if isinstance(jobs_data.company_id, int):
        return jobs_data
    return False


async def check_address_for_company(address: str, company_name: str):
    """
    Функция, поверяет о наличии вдреса для этой компании
    :param address:
    :param company_name:
    :return:
    """
    async with get_db_session() as session:
        address_data = await session.execute(
            select(Address)
            .join(Address.company)
            .options(joinedload(Address.company))
            .where(
                and_(
                    Address.address == address,
                    Company.company_name == company_name,
                )
            )
        )
        address = address_data.scalar_one_or_none()
    return address is not None


async def check_address_def(address: str):
    """
    Функция по проверке о наличии адреса
    :param address:
    :return:
    """
    async with get_db_session() as session:
        address_data = await session.execute(
            select(Address).where(Address.address == address)
        )
        address = address_data.scalar_one_or_none()
    if address is not None:
        return address
    return False


async def add_address(address: str, empl_id: int) -> list:
    """
    Функция, добавляющая аддресс к обслуживающей компании, если его нет
    :param address: адрес обслуживаемого объекта
    :param empl_id:
    :return:
    """
    jobs_data = await get_last_company_by_empl(empl_id=empl_id)
    check_address = await check_address_def(address=address)
    async with get_db_session() as session:
        if not check_address:
            address_data = await session.execute(
                insert(Address)
                .values(
                    address=address,
                    company_id=jobs_data.company.id,
                )
                .returning(Address)
            )
            check_address = address_data.scalar_one_or_none()
            await session.commit()
        answer_data = await session.execute(
            select(Jobs)
            .join(Jobs.staff)
            .join(Jobs.company)
            .options(
                joinedload(Jobs.staff),
                joinedload(Jobs.company),
            )
            .where(Staff.tel_id == empl_id)
            .order_by(desc(Jobs.id))
            .limit(1)
        )
        answer = answer_data.scalar_one_or_none()
        await session.execute(
            update(Jobs)
            .where(Jobs.id == answer.id)
            .values(address_id=check_address.id)
        )
        await session.execute(
            update(Company)
            .where(Company.id == answer.company.id)
            .values(tasks=Company.tasks + 1)
        )
        await session.commit()
    return [
        answer.id,
        answer.company.company_name,
        check_address.address,
        answer.staff.name,
        answer.staff.surname,
    ]


async def get_all_job_by_empl(empl_id: int) -> bool | list:
    """
    Функция, возвращает список действющих заявок работника, либо false, если их нет
    :param empl_id:
    :return:
    """
    async with get_db_session() as session:
        job_data = await session.execute(
            select(Jobs)
            .join(Jobs.company)
            .join(Jobs.staff)
            .join(Jobs.address)
            .join(Jobs.type)
            .options(
                joinedload(Jobs.staff),
                joinedload(Jobs.company),
                joinedload(Jobs.address),
                joinedload(Jobs.type),
            )
            .where(and_(Staff.tel_id == empl_id, Jobs.time_close.is_(None)))
        )
        jobs = job_data.scalars().all()
    if jobs:
        return [
            (
                job.id,
                job.company.company_name,
                job.address.address,
                job.type.job_name,
            )
            for job in jobs
        ]
    return False


async def close_task_by_empl(task_id: int) -> list:
    """
    Функция, возвращает список данных по закрытой заявке и закрывает заявку
    :param task_id:
    :return:
    """
    async with get_db_session() as session:
        await session.execute(
            update(Jobs)
            .where(Jobs.id == task_id)
            .values(time_close=datetime.datetime.today())
        )
        await session.commit()
        job_data = await session.execute(
            select(Jobs)
            .join(Jobs.staff)
            .join(Jobs.company)
            .join(Jobs.address)
            .options(
                joinedload(Jobs.staff),
                joinedload(Jobs.company),
                joinedload(Jobs.address),
            )
            .where(Jobs.id == task_id)
        )
        job = job_data.scalars().first()
    return [
        job.id,
        job.company.company_name,
        job.address.address,
        datetime.datetime.strftime(job.time_add, "%H:%M %d.%m.%Y г."),
        datetime.datetime.strftime(job.time_close, "%H:%M %d.%m.%Y г."),
        job.staff.name,
        job.staff.surname,
    ]


async def get_company_name(job_id: int) -> str:
    """
    Функция возвращает название компании, по id заявки
    :param job_id:
    :return:
    """
    async with get_db_session() as session:
        result = await session.execute(
            select(Company.company_name)
            .join(Company.jobs)
            .where(Jobs.id == job_id)
        )
        company_name = result.scalar_one_or_none()
    return company_name


async def insert_new_job_change(job_id: int):
    """
    Фунция, которая создает новую запись в модели job_change
    :param job_id:
    :return:
    """
    async with get_db_session() as session:
        job_data = await session.execute(
            select(Jobs)
            .join(Jobs.company)
            .join(Jobs.type)
            .join(Jobs.address)
            .options(
                joinedload(Jobs.company),
                joinedload(Jobs.type),
                joinedload(Jobs.address),
            )
            .where(Jobs.id == job_id)
        )
        job = job_data.scalars().first()
        await session.execute(
            insert(ChangeJobs).values(
                employee_id=job.employee,
                jobs_id=job_id,
                job_id_old=job.type.id,
                job_id_new=job.type.id,
                company_old_id=job.company.id,
                company_new_id=job.company.id,
                address_old_id=job.address.id,
                address_new_id=job.address.id,
                time_init=job.time_add,
            )
        )
        await session.commit()


async def check_company(company_name: str):
    """
    Функция, проверяет наличие компании по названию
    :param company_name:
    :return:
    """
    async with get_db_session() as session:
        company_data = await session.execute(
            select(Company).where(Company.company_name == company_name)
        )
        company = company_data.scalar_one_or_none()
    return company if company is not None else False


async def update_company_for_task(company_id: int, task_id: int):
    """
    Функция, меняет занчение id компании в заявке
    :param task_id:
    :param company_id:
    :return:
    """
    async with get_db_session() as session:
        await session.execute(
            update(Jobs)
            .where(Jobs.id == task_id)
            .values(company_id=company_id)
        )
        change_data = await session.execute(
            select(ChangeJobs)
            .where(ChangeJobs.jobs_id == task_id)
            .order_by(desc(ChangeJobs.id))
            .limit(1)
        )
        change = change_data.scalar_one_or_none()
        await session.execute(
            update(ChangeJobs)
            .where(ChangeJobs.id == change.id)
            .values(company_new_id=company_id)
        )
        await session.execute(
            update(Company)
            .where(Company.id == company_id)
            .values(tasks=Company.tasks + 1)
        )
        await session.commit()


async def check_job(job_name: str):
    """
    Функция проверяет есть таокй вид работ в базе данных
    :param job_name:
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            select(JobType.id).where(JobType.job_name == job_name)
        )
        result = result_data.scalar_one_or_none()
    return isinstance(result, int)


async def change_task_by_company(company_name: str):
    """
    Функция меняяет количество задач у компаниим на -1
    :param company_name:
    :return:
    """
    async with get_db_session() as session:
        await session.execute(
            update(Company)
            .where(Company.company_name == company_name)
            .values(tasks=Company.tasks - 1)
        )
        await session.commit()


async def update_company_name(empl_id: int, new_name: str):
    """
    Функция, которая добавляет название компании в запись о замене данных
    :param new_name:
    :param empl_id:
    :return:
    """
    async with get_db_session() as session:
        job_data = await session.execute(
            select(ChangeJobs)
            .join(ChangeJobs.staff)
            .options(joinedload(ChangeJobs.staff))
            .where(Staff.tel_id == empl_id)
            .order_by(desc(ChangeJobs.id))
            .limit(1)
        )
        job = job_data.scalars().first()
        new_company_data = await session.execute(
            insert(Company).values(company_name=new_name).returning(Company)
        )
        new_company_id = new_company_data.scalar_one().id
        change_jobs_data = await session.execute(
            update(ChangeJobs)
            .where(ChangeJobs.id == job.id)
            .values(company_new_id=new_company_id)
            .returning(ChangeJobs)
        )
        change_job = change_jobs_data.scalar()
        await session.execute(
            update(Jobs)
            .where(Jobs.id == change_job.jobs_id)
            .values(company_id=new_company_id)
        )
        await session.commit()


async def get_address_name_update(empl_id: int) -> str:
    """
    Функция,которая возвращает значение адреса по последней изменяемой задаче
    :return:
    """
    company_address = aliased(Address)

    async with get_db_session() as session:
        address_data = await session.execute(
            select(
                ChangeJobs, company_address.address.label("company_address")
            )
            .join(ChangeJobs.staff)
            .join(
                company_address,
                ChangeJobs.address_new_id == company_address.id,
            )
            .options(
                joinedload(ChangeJobs.staff),
                joinedload(ChangeJobs.address_new),
            )
            .where(Staff.tel_id == empl_id)
            .order_by(desc(ChangeJobs.id))
            .limit(1)
        )
        address_data = address_data.first()
        (change_job, address) = address_data
    return address


async def get_address_by_empl_id_for_update(company_name: int) -> list | bool:
    """
    Функиця, возвращает список адресов компании или false при их отсутствии
    :return:
    """
    async with get_db_session() as session:
        address_data = await session.execute(
            select(Address)
            .join(Address.company)
            .options(joinedload(Address.company))
            .where(Company.company_name == company_name)
        )
        if address_data:
            return [
                address.address for address in address_data.scalars().all()
            ]
        return False


async def update_address_for_company(
    new_address: str, empl_id: int, new_company=False
):
    """
    Функция, которая обновляет адрес в модели компании и изменении работы
    :param new_company:
    :param new_address:
    :param empl_id:
    :return:
    """
    async with get_db_session() as session:
        company_data = await session.execute(
            select(ChangeJobs)
            .join(ChangeJobs.staff)
            .options(joinedload(ChangeJobs.staff))
            .where(Staff.tel_id == empl_id)
            .order_by(desc(ChangeJobs.id))
            .limit(1)
        )
        row = company_data.scalars().first()
        if new_company:
            new_address_data = await session.execute(
                insert(Address)
                .values(company_id=row.company_new_id, address=new_address)
                .returning(Address)
            )
            new_address = new_address_data.scalar()
        else:
            new_address_data = await session.execute(
                select(Address).where(Address.address == new_address)
            )
            new_address = new_address_data.scalar()
        await session.execute(
            update(Jobs)
            .where(Jobs.id == row.jobs_id)
            .values(address_id=new_address.id)
        )
        await session.execute(
            update(ChangeJobs)
            .where(ChangeJobs.id == row.id)
            .values(address_new_id=new_address.id)
        )
        await session.commit()


async def get_job_type_update(empl_id: int) -> str:
    """
    Функция, которая возвращает тип работы по данной заявке
    :param empl_id:
    :return:
    """
    async with get_db_session() as session:
        job_type_data = await session.execute(
            select(
                ChangeJobs,
            )
            .join(ChangeJobs.staff)
            .join(ChangeJobs.job_new)
            .options(
                joinedload(ChangeJobs.staff), joinedload(ChangeJobs.job_new)
            )
            .where(Staff.tel_id == empl_id)
            .order_by(desc(ChangeJobs.id))
            .limit(1)
        )
        job_type = job_type_data.scalars().first()
    return job_type.job_new.job_name


async def set_time_change(empl_id: int):
    """
    Функция, которая добавляет знаачени завершенного времени ыормирования функции
    :param empl_id:
    :return:
    """

    async with get_db_session() as session:
        change_jobs_data = await session.execute(
            select(ChangeJobs)
            .options(joinedload(ChangeJobs.staff))
            .where(and_(Staff.tel_id == empl_id, Staff.status == 2))
            .order_by(desc(ChangeJobs.id))
            .limit(1)
        )
        change_jobs = change_jobs_data.scalars().first()
        await session.execute(
            update(ChangeJobs)
            .where(ChangeJobs.id == change_jobs.id)
            .values(time_change=datetime.datetime.today())
        )
        await session.commit()


async def update_job_type(empl_id: int, job_type: str):
    """
    Функция, которая обновляет вид работ, записанный в базе данных
    :param job_type:
    :param empl_id:
    :return:
    """

    async with get_db_session() as session:
        job_type_id_data = await session.execute(
            select(JobType.id).where(JobType.job_name == job_type)
        )
        job_type_id = job_type_id_data.scalar()
        change_jobs_data = await session.execute(
            select(ChangeJobs)
            .join(ChangeJobs.staff)
            .options(joinedload(ChangeJobs.staff))
            .where(and_(Staff.tel_id == empl_id, Staff.status == 2))
            .order_by(desc(ChangeJobs.id))
            .limit(1)
        )
        change_jobs = change_jobs_data.scalars().first()
        await session.execute(
            update(ChangeJobs)
            .where(ChangeJobs.id == change_jobs.id)
            .values(
                job_id_new=job_type_id, time_change=datetime.datetime.today()
            )
        )
        await session.execute(
            update(Jobs)
            .where(Jobs.id == change_jobs.jobs_id)
            .values(job_id=job_type_id)
        )
        await session.commit()


async def get_new_job(empl_id: int) -> list:
    """
    Функция, которая возращает последнюю измененную заявку
    :param empl_id:
    :return:
    """
    company_old = aliased(Company)
    company_new = aliased(Company)
    job_name_old = aliased(JobType)
    job_name_new = aliased(JobType)
    address_old = aliased(Address)
    address_new = aliased(Address)

    async with get_db_session() as session:
        jobs_data = await session.execute(
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
            .join(ChangeJobs.job_new)
            .join(company_old, ChangeJobs.company_old_id == company_old.id)
            .outerjoin(
                company_new, ChangeJobs.company_new_id == company_new.id
            )
            .join(job_name_old, ChangeJobs.job_id_old == job_name_old.id)
            .outerjoin(job_name_new, ChangeJobs.job_id_new == job_name_new.id)
            .join(address_old, ChangeJobs.address_old_id == address_old.id)
            .outerjoin(
                address_new, ChangeJobs.address_new_id == address_new.id
            )
            .options(
                joinedload(ChangeJobs.staff),
                joinedload(ChangeJobs.jobs),
                joinedload(ChangeJobs.job_new),
            )
            .where(and_(Staff.tel_id == empl_id, Staff.status == 2))
            .order_by(desc(ChangeJobs.id))
            .limit(1)
        )
        row = jobs_data.first()
    (
        change_job,
        old_name,
        new_name,
        job_name_old,
        job_name_new,
        address_old,
        address_new,
    ) = row
    return [
        change_job.jobs.id,
        [job_name_old, job_name_new],
        [old_name, new_name],
        [address_old, address_new],
        [
            datetime.datetime.strftime(
                change_job.time_init, "%H:%M %d.%m.%Y г."
            ),
            datetime.datetime.strftime(
                change_job.time_change, "%H:%M %d.%m.%Y г."
            ),
        ],
        [change_job.staff.name, change_job.staff.surname],
    ]
