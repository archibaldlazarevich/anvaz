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

from sqlalchemy import select, update, and_, insert


async def get_empl_if_exist(empl_id: int):
    """
    Функция проверяет есть ли пользователь в базе данных
    :param empl_id:
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            select(Staff).where(
                (Staff.tel_id == empl_id),
            )
        )
        result = result_data.scalar_one_or_none()
    return True if not result else False


async def insert_new_staff(name: str, surname: str, empl_id: int):
    """
    Функция добавляет нового пользователя
    :param name:
    :param surname:
    :param empl_id:
    :return:
    """

    async with get_db_session() as session:
        await session.execute(
            insert(Staff).values(
                status=1, name=name, surname=surname, tel_id=empl_id
            )
        )
        await session.commit()


async def add_direct(name: str, surname: str) -> int:
    """
    Функция для изменения статуса пользователя на статус начальника
    :param name: Имя пользователя
    :param surname: Фамилия пользователя
    :return: int статус
    """
    async with get_db_session() as session:
        await session.execute(
            update(Staff)
            .where(and_(Staff.name == name, Staff.surname == surname))
            .values(status=3)
        )
        director_data = await session.execute(
            select(Staff.status).where(
                and_(Staff.name == name, Staff.surname == surname)
            )
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
        await session.execute(
            update(Staff)
            .where(and_(Staff.name == name, Staff.surname == surname))
            .values(status=2)
        )
        emp_data = await session.execute(
            select(Staff.status).where(
                and_(Staff.name == name, Staff.surname == surname)
            )
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
        await session.execute(insert(JobType).values(job_name=job_name))
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


async def get_all_del_company() -> list:
    """
    Функция для получения все неактивных компаний
    :return:
    """
    async with get_db_session() as session:
        all_company_data = await session.execute(
            select(Company).where(Company.status == 0)
        )
        all_company = all_company_data.scalars()
    return [company.company_name for company in all_company]


async def return_del_job(job_name: str):
    """
    Функция по возвращению вида работ в активные
    :param job_name:
    :return:
    """

    async with get_db_session() as session:
        job_data = await session.execute(
            select(JobType).where(JobType.job_name == job_name)
        )
        job = job_data.scalar_one_or_none()
        if job:
            await session.execute(
                update(JobType)
                .where(JobType.job_name == job_name)
                .values(active=1)
            )
            await session.commit()
            return True
        return False


async def return_del_company(company_name: str):
    """
    Функция, возравщет компанию из неактвных
    :param company_name:
    :return:
    """
    async with get_db_session() as session:
        company_data = await session.execute(
            select(Company).where(Company.company_name == company_name)
        )
        company = company_data.scalar_one_or_none()
        if company:
            await session.execute(
                update(Company)
                .where(Company.id == company.id)
                .values(status=1)
            )
            await session.execute(
                update(Address)
                .where(Address.company_id == company.id)
                .values(status=1)
            )
            await session.commit()
            return True
        return False


async def rm_direct(name: str, surname: str) -> bool:
    """
    Функция для изменения статуса начальника на статус пользователя
    :param name: Имя начальникиа
    :param surname: Фамилия начальника
    :return: int статус
    """
    async with get_db_session() as session:
        await session.execute(
            update(Staff)
            .where(and_(Staff.name == name, Staff.surname == surname))
            .values(status=1)
        )
        director_data = await session.execute(
            select(Staff.status).where(
                and_(Staff.name == name, Staff.surname == surname)
            )
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
        await session.execute(
            update(Staff)
            .where(and_(Staff.name == name, Staff.surname == surname))
            .values(status=1)
        )
        empl_data = await session.execute(
            select(Staff.status).where(
                and_(Staff.name == name, Staff.surname == surname)
            )
        )
        await session.commit()
        employee = empl_data.scalar_one_or_none()
    return employee == 1


async def get_tel_id(name: str, surname: str):
    """
    Функция возвращает id телеграмма сотрудника по его имени и фамилии
    :param name:
    :param surname:
    :return:
    """
    async with get_db_session() as session:
        tel_id_data = await session.execute(
            select(Staff).where(
                and_(Staff.name == name, Staff.surname == surname)
            )
        )
        tel_id = tel_id_data.scalar_one_or_none()
    return tel_id


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
        await session.execute(
            update(Staff)
            .where(and_(Staff.name == name, Staff.surname == surname))
            .values(status=4)
        )
        empl_data = await session.execute(
            select(Staff).where(
                and_(Staff.name == name, Staff.surname == surname)
            )
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
        await session.execute(
            update(Staff)
            .where(and_(Staff.name == name, Staff.surname == surname))
            .values(status=1)
        )
        empl_data = await session.execute(
            select(Staff.status).where(
                and_(Staff.name == name, Staff.surname == surname)
            )
        )
        await session.commit()
        employee = empl_data.scalar_one_or_none()
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


async def get_busy_empl_without_spec_empl(name: str, surname: str):
    """
    Функция для проверки о наличии работников в базе данных кроме предоставленного
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
                and_(Company.company_name != company_name, Company.status == 1)
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
        job_type_data = await session.execute(
            select(JobType).where(JobType.active == 1)
        )
    return [job_type.job_name for job_type in job_type_data.scalars().all()]


async def get_all_company_name():
    """
    Функция, возвращающая список названий компаний, которые есть в бд
    :return:
    """
    async with get_db_session() as session:
        company_name_data = await session.execute(
            select(Company).where(Company.status == 1)
        )
    return [
        company_name.company_name
        for company_name in company_name_data.scalars().all()
    ]


async def get_all_active_company_name():
    """
    Функция, возвращающая список названий компаний, которые есть в бд
    :return:
    """
    async with get_db_session() as session:
        company_name_data = await session.execute(
            select(Address)
            .join(Address.company)
            .options(joinedload(Address.company))
            .where(and_(Company.status == 1, Address.status == 1))
        )
    return [
        company_name.company.company_name
        for company_name in company_name_data.scalars().all()
    ]


async def add_new_address(company_name: str, address: str):
    """
    Функция добавляет адрес к компании
    :param company_name:
    :param address:
    :return:
    """
    async with get_db_session() as session:
        company_data = await session.execute(
            select(Company.id).where(Company.company_name == company_name)
        )
        company_id = company_data.scalar_one_or_none()
        await session.execute(
            insert(Address).values(address=address, company_id=company_id)
        )
        await session.commit()


async def check_address_for_company_all(address: str, company_name: str):
    """
    Функция, поверяет о наличии адреса для этой компании
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
                    Company.status == 1,
                )
            )
        )
        address = address_data.scalar_one_or_none()
    if address is not None:
        if address.status == 1:
            return address
        return 3
    return False


async def check_if_ban_address_for_company(address: str, company_name: str):
    """
    Функция, поверяет о наличии неактивного адреса для этой компании
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
                    Address.status == 0,
                    Company.company_name == company_name,
                    Company.status == 1,
                )
            )
        )
        address = address_data.scalar_one_or_none()
    return address is not None


async def return_address(company_name: str, address: str):
    """
    Функция, переводи адрес в автиынй режим
    :param company_name:
    :param address:
    :return:
    """
    async with get_db_session() as session:
        address_data = await session.execute(
            select(Address)
            .join(Address.company)
            .where(
                and_(
                    Address.address == address,
                    Company.company_name == company_name,
                    Address.status == 0,
                )
            )
        )
        address_id = address_data.scalar_one_or_none().id
        await session.execute(
            update(Address).where(Address.id == address_id).values(status=1)
        )
        await session.commit()


async def rm_address(company_name: str, address: str):
    """
    Функция, переводи адрес в неактивный режим
    :param company_name:
    :param address:
    :return:
    """
    async with get_db_session() as session:
        address_data = await session.execute(
            select(Address)
            .join(Address.company)
            .where(
                and_(
                    Address.address == address,
                    Company.company_name == company_name,
                    Address.status == 1,
                )
            )
        )
        address_id = address_data.scalar_one_or_none().id
        await session.execute(
            update(Address).where(Address.id == address_id).values(status=0)
        )
        await session.commit()


async def check_address_for_company(address: str, company_name: str):
    """
    Функция, поверяет о наличии адреса для этой компании
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
                    Address.status == 1,
                    Company.status == 1,
                )
            )
        )
        address = address_data.scalar_one_or_none()
    return address is not None


async def get_address_company_id(address: str, company_name: str):
    """
    Функуия возвращает id комапнии адреса по названию адреса
    :param company_name:
    :param address:
    :return:
    """
    async with get_db_session() as session:
        company_data = await session.execute(
            select(Address)
            .join(Address.company)
            .options(joinedload(Address.company))
            .where(
                and_(
                    Address.address == address,
                    Address.status == 1,
                    Company.company_name == company_name,
                    Company.status == 1,
                )
            )
        )
        company_data = company_data.scalar_one_or_none()
    return [company_data.company_id, company_data.id]


async def get_job_id(job_name: str):
    """
    Функция возвращает тип работы
    :param job_name:
    :return:
    """
    async with get_db_session() as session:
        job_data = await session.execute(
            select(JobType.id).where(JobType.job_name == job_name)
        )
        job = job_data.scalar_one_or_none()
    return job


async def get_empl_id(empl_id: int):
    """
    Функция, возращает id пользваоетеля по его id телеграмма
    :param empl_id:
    :return:
    """
    async with get_db_session() as session:
        empl_data = await session.execute(
            select(Staff.id).where(
                and_(Staff.tel_id == empl_id, Staff.status == 2)
            )
        )
        empl_id = empl_data.scalar_one_or_none()
    return empl_id


async def add_new_job(
    address_name: str, job_name: str, empl_id: int, company_name: str
):
    """
    Функция , добавляющая новую заявку
    :param company_name:
    :param empl_id:
    :param address_name:
    :param job_name:
    :return:
    """
    company_id, address_id = await get_address_company_id(
        address=address_name, company_name=company_name
    )
    job_id = await get_job_id(job_name=job_name)
    staff_id = await get_empl_id(empl_id=empl_id)
    async with get_db_session() as session:
        await session.execute(
            insert(Jobs).values(
                job_id=job_id,
                company_id=company_id,
                address_id=address_id,
                employee=staff_id,
            )
        )
        await session.execute(
            update(Company)
            .where(Company.id == company_id)
            .values(tasks=Company.tasks + 1)
        )
        new_job_data = await session.execute(
            select(Jobs)
            .join(Jobs.staff)
            .join(Jobs.company)
            .join(Jobs.address)
            .join(Jobs.type)
            .options(
                joinedload(Jobs.staff),
                joinedload(Jobs.company),
                joinedload(Jobs.address),
                joinedload(Jobs.type),
            )
            .where(Jobs.employee == staff_id)
            .order_by(desc(Jobs.id))
            .limit(1)
        )
        answer = new_job_data.scalar_one_or_none()
        await session.commit()
        return [
            answer.id,
            answer.company.company_name,
            answer.address.address,
            answer.staff.name,
            answer.staff.surname,
            answer.type.job_name,
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


async def get_all_address_for_company(company_name: str):
    """
    Возвращает список адресов по компании
    :param company_name:
    :return:
    """
    async with get_db_session() as session:
        address_data = await session.execute(
            select(Address)
            .join(Address.company)
            .options(joinedload(Address.company))
            .where(
                and_(Company.company_name == company_name, Address.status == 1)
            )
        )
        address = address_data.scalars().all()
    return [address.address for address in address]


async def rm_company(company_name: str):
    """
    Функция переводи компанию и ее адреса в неактивный режим
    :param company_name:
    :return:
    """
    async with get_db_session() as session:
        company_id_data = await session.execute(
            select(Company).where(Company.company_name == company_name)
        )
        company_id = company_id_data.scalar_one_or_none().id
        await session.execute(
            update(Company).where(Company.id == company_id).values(status=0)
        )
        await session.execute(
            update(Address)
            .where(Address.company_id == company_id)
            .values(status=0)
        )
        await session.commit()


async def check_all_company(company_name: str):
    """
    Функция, проверяет наличие компании по названию
    :param company_name:
    :return:
    """
    async with get_db_session() as session:
        company_data = await session.execute(
            select(Company).where(
                and_(
                    Company.company_name == company_name,
                )
            )
        )
        company = company_data.scalar_one_or_none()
    if company is not None:
        if company.status == 1:
            return company
        elif company.status == 0:
            return 3
    return False


async def get_all_company():
    """
    Функция возвращает все компании
    :return:
    """
    async with get_db_session() as session:
        company_data = await session.execute(
            select(Company).where(Company.status == 1)
        )
        company_data = company_data.scalars().all()
    return (
        [company.company_name for company in company_data]
        if company_data
        else None
    )


async def add_company(company_name: str):
    """
    Функция, для добавления компании в базу данных
    :param company_name:
    :return:
    """
    async with get_db_session() as session:
        await session.execute(
            insert(Company).values(company_name=company_name)
        )
        await session.commit()


async def check_active_address_for_company(company_name: str):
    """
    Функиия, возвращает активные адреса для компании
    :param company_name:
    :return:
    """
    async with get_db_session() as session:
        address_data = await session.execute(
            select(Address)
            .join(Address.company)
            .options(joinedload(Address.company))
            .where(
                and_(Company.company_name == company_name, Address.status == 1)
            )
        )
        address_all = address_data.scalars().all()
    return (
        [address.address for address in address_all] if address_all else False
    )


async def check_ban_address_for_company(company_name: str):
    """
    Функиия, возвращает пассивные адреса для компании
    :param company_name:
    :return:
    """
    async with get_db_session() as session:
        address_data = await session.execute(
            select(Address)
            .join(Address.company)
            .options(joinedload(Address.company))
            .where(
                and_(Company.company_name == company_name, Address.status == 0)
            )
        )
        address_all = address_data.scalars().all()
    return (
        [address.address for address in address_all] if address_all else False
    )


async def check_job(job_name: str):
    """
    Функция проверяет есть такой вид работ в базе данных
    :param job_name:
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            select(JobType.id).where(JobType.job_name == job_name)
        )
        result = result_data.scalar_one_or_none()
    return isinstance(result, int)


async def get_task_all_data(task_id: int):
    """
    Функция, возвращает данные по задаче
    :param task_id:
    :return:
    """
    async with get_db_session() as session:
        task_data = await session.execute(
            select(Jobs)
            .join(Jobs.company)
            .join(Jobs.address)
            .join(Jobs.type)
            .options(
                joinedload(Jobs.company),
                joinedload(Jobs.address),
                joinedload(Jobs.type),
            )
            .where(Jobs.id == task_id)
        )
        task = task_data.scalar_one_or_none()
        return {
            "task_id": task_id,
            "company_data": {
                "id": task.company_id,
                "name": task.company.company_name,
            },
            "address_data": {
                "id": task.address_id,
                "name": task.address.address,
            },
            "type_data": {
                "id": task.job_id,
                "name": task.type.job_name,
            },
            "time_add": task.time_add,
        }


async def get_address_by_empl_id_for_update(company_name: str) -> list | bool:
    """
    Функиця, возвращает список адресов компании или false при их отсутствии
    :return:
    """
    async with get_db_session() as session:
        address_data = await session.execute(
            select(Address)
            .join(Address.company)
            .options(joinedload(Address.company))
            .where(
                and_(
                    Company.company_name == company_name,
                    Company.status == 1,
                    Address.status == 1,
                )
            )
        )
        return (
            [address.address for address in address_data.scalars().all()]
            if address_data
            else False
        )


async def change_task_count_company(old_id: int, new_id: int):
    """
    Функци меняет количсвто task  укомпаний
    :param old_id:
    :param new_id:
    :return:
    """
    async with get_db_session() as session:
        await session.execute(
            update(Company)
            .where(Company.id == old_id)
            .values(tasks=Company.tasks - 1)
        )
        await session.execute(
            update(Company)
            .where(Company.id == new_id)
            .values(tasks=Company.tasks + 1)
        )
        await session.commit()


async def create_change_jobs(
    old_data: dict,
    new_company_id: int,
    new_address_id: int,
    new_job_id: int,
    empl_id: int,
):
    """
    Функция, котрая добавляет сущность изменения в таблицу changejobs
    :param old_data:
    :param new_company_id:
    :param new_address_id:
    :param new_job_id:
    :param empl_id:
    :return:
    """
    async with get_db_session() as session:
        await session.execute(
            insert(ChangeJobs).values(
                employee_id=empl_id,
                jobs_id=old_data["task_id"],
                job_id_old=old_data["type_data"]["id"],
                job_id_new=new_job_id,
                company_old_id=old_data["company_data"]["id"],
                company_new_id=new_company_id,
                address_old_id=old_data["address_data"]["id"],
                address_new_id=new_address_id,
                time_change=datetime.datetime.now(),
                time_init=old_data["time_add"],
            )
        )
        job_change_id_data = await session.execute(
            select(ChangeJobs)
            .where(and_(ChangeJobs.employee_id == empl_id))
            .order_by(desc(ChangeJobs.id))
            .limit(1)
        )
        job_change_id = job_change_id_data.scalar_one_or_none().id
        await session.commit()
    return job_change_id


async def change_job_data(
    job_id: int, company_id: int, job_type_id: int, address_id: int
):
    """
    Функция, меняет значения в работе
    :param job_id:
    :param company_id:
    :param job_type_id:
    :param address_id:
    :return:
    """
    async with get_db_session() as session:
        await session.execute(
            update(Jobs)
            .where(Jobs.id == job_id)
            .values(
                job_id=job_type_id,
                company_id=company_id,
                address_id=address_id,
            )
        )
        await session.commit()


async def add_change_job(
    old_data: dict,
    new_company: str,
    new_address: str,
    new_job: str,
    empl_id: int,
):
    """
    Функция, которая добавляет изменение к существующей работе
    :param empl_id:
    :param old_data:
    :param new_company:
    :param new_address:
    :param new_job:
    :return:
    """
    company_id, address_id = await get_address_company_id(
        address=new_address, company_name=new_company
    )
    job_type_id = await get_job_id(job_name=new_job)
    staff_id = await get_empl_id(empl_id=empl_id)
    if company_id != old_data["company_data"]["id"]:
        await change_task_count_company(
            old_id=old_data["company_data"]["id"], new_id=company_id
        )
    job_change_id = await create_change_jobs(
        old_data=old_data,
        new_company_id=company_id,
        new_address_id=address_id,
        new_job_id=job_type_id,
        empl_id=staff_id,
    )
    await change_job_data(
        job_id=old_data["task_id"],
        company_id=company_id,
        job_type_id=job_type_id,
        address_id=address_id,
    )
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
            .where(ChangeJobs.id == job_change_id)
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
