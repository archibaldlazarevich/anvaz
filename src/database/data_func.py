from src.database.create_db import get_db_session
from src.database.models import Staff, JobType, Admin

from sqlalchemy import select, update, and_, insert, delete


async def add_direct(name: str, surname: str) -> int:
    """
    Функция для изменения статуса пользователя на статус начальника
    :param name: Имя пользователя
    :param surname: Фамилия пользователя
    :return: int статус
    """
    async with get_db_session() as session:
        director_data = await session.execute(update(Staff).filter(
                and_(Staff.name == name, Staff.surname == surname)).values(status = 3).returning(Staff)
        )
        await session.commit()
        director = director_data.scalar().status
    return director


async def get_all_non_employee() -> list:
    """
    Функция для поиска всех не работников в базе данных
    :return:
    """
    async with get_db_session() as session:
        staff_data = await session.execute(select(Staff).where(Staff.status == 1))
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
        emp_data = await session.execute(update(Staff).filter(
                and_(Staff.name == name, Staff.surname == surname)).values(status = 2).returning(Staff)
        )
        await session.commit()
        emp = emp_data.scalar()
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
        all_dir_data = await session.execute(select(Staff).where(Staff.status == 3))
        all_dir_data = all_dir_data.scalars()
    return [(person.name, person.surname) for person in all_dir_data]


async def get_all_emp() -> list:
    """
    Функция по получению всех работников в б.д.
    :return:
    """
    async with get_db_session() as session:
        all_emp_data = await session.execute(select(Staff).where(Staff.status == 2))
        all_emp_data = all_emp_data.scalars()
    return [(person.name, person.surname) for person in all_emp_data]

async def get_all_jobs() -> list:
    """
    Функция по получению всех видов работ в б.д.
    :return:
    """
    async with get_db_session() as session:
        all_jobs_data = await session.execute(select(JobType))
        all_jobs_data = all_jobs_data.scalars()
    return [job.job_name for job in all_jobs_data]


async def rm_direct(name: str, surname: str) -> bool:
    """
    Функция для изменения статуса начальника на статус пользователя
    :param name: Имя начальникиа
    :param surname: Фамилия начальника
    :return: int статус
    """
    async with get_db_session() as session:
        director_data = await session.execute(update(Staff).filter(
                and_(Staff.name == name, Staff.surname == surname)).values(status = 1).returning(Staff)
        )
        await session.commit()
        director = director_data.scalar().status
    if director == 1:
        return True
    return False


async def rm_employee(name: str, surname: str) -> bool:
    """
    Функция для изменения статуса работника на статус пользователя
    :param name: Имя работника
    :param surname: Фамилия работника
    :return: int статус
    """
    async with get_db_session() as session:
        empl_data = await session.execute(update(Staff).filter(
                and_(Staff.name == name, Staff.surname == surname)).values(status = 1).returning(Staff)
        )
        await session.commit()
        employee = empl_data.scalar().status
    if employee == 1:
        return True
    return False

async def rm_job(job_name: str) -> None:
    """
    Функция для удаления вида работы
    :param job_name: наименование работы
    :return: None
    """
    async with get_db_session() as session:
        await session.execute(delete(JobType).where(JobType.job_name == job_name))
        await session.commit()


async def rm_non_staff(name: str, surname: str) -> bool:
    """
    Функция для удаления пользователя из списка (статус - 4)
    :param job_name: наименование работы
    :return: None
    """
    async with get_db_session() as session:
        empl_data = await session.execute(update(Staff).filter(
                and_(Staff.name == name, Staff.surname == surname)).values(status = 4).returning(Staff)
        )
        await session.commit()
        employee = empl_data.scalar().status
    if employee == 4:
        return True
    return False

async def get_all_dell() -> list:
    """
    Функция по получению всех забаненных пользователей
    :return:
    """
    async with get_db_session() as session:
        all_emp_data = await session.execute(select(Staff).where(Staff.status == 4))
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
        empl_data = await session.execute(update(Staff).filter(
                and_(Staff.name == name, Staff.surname == surname)).values(status = 1).returning(Staff)
        )
        await session.commit()
        employee = empl_data.scalar().status
    if employee == 1:
        return True
    return False


async def get_admin_id() -> int:
    """
    Функция для получения id админа
    :return:
    """
    async with get_db_session() as session:
        data_admin = await session.execute(select(Admin))
        data_admin_id = data_admin.scalar().tel_ad_id
    return data_admin_id

