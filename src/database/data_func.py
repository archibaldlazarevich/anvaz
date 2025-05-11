from traceback import print_tb

from sqlalchemy.orm import joinedload
import datetime
from sqlalchemy import func, case

from src.database.create_db import get_db_session
from src.database.models import Staff, JobType, Admin, Jobs

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
            .filter(and_(Staff.name == name, Staff.surname == surname))
            .values(status=3)
            .returning(Staff)
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
        staff_data = await session.execute(
            select(Staff).where(Staff.status == 1)
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
            .filter(and_(Staff.name == name, Staff.surname == surname))
            .values(status=2)
            .returning(Staff)
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
        director_data = await session.execute(
            update(Staff)
            .filter(and_(Staff.name == name, Staff.surname == surname))
            .values(status=1)
            .returning(Staff)
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
        empl_data = await session.execute(
            update(Staff)
            .filter(and_(Staff.name == name, Staff.surname == surname))
            .values(status=1)
            .returning(Staff)
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
        await session.execute(
            delete(JobType).where(JobType.job_name == job_name)
        )
        await session.commit()


async def rm_non_staff(name: str, surname: str) -> bool:
    """
    Функция для удаления пользователя из списка (статус - 4)
    :param job_name: наименование работы
    :return: None
    """
    async with get_db_session() as session:
        empl_data = await session.execute(
            update(Staff)
            .filter(and_(Staff.name == name, Staff.surname == surname))
            .values(status=4)
            .returning(Staff)
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
            .filter(and_(Staff.name == name, Staff.surname == surname))
            .values(status=1)
            .returning(Staff)
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


async def get_all_dir_id() -> list[int]:
    """
    Функция для получения id начальников в базе данных
    :return:
    """
    async with get_db_session() as session:
        data_dir = await session.execute(
            select(Staff).where(Staff.status == 3)
        )
        dirs_id = [dir.tel_id for dir in data_dir.scalars()]
    return dirs_id




async def get_all_proc_jobs() -> list:
    """
    Функция, возвращающия список действующих заявок
    :return:
    """
    async with get_db_session() as session:
        proc_data = await session.execute(
            select(Jobs)
            .where(Jobs.time_close.is_(None))
            .options(
                joinedload(Jobs.staff),
                joinedload(Jobs.type),
            )
            .group_by(Jobs.id)
            .order_by(Jobs.id)
        )
        procs = proc_data.scalars().all()
    return [
        (
            proc.id,
            proc.type.job_name,
            proc.company_name,
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
            select(Staff).filter(
                and_(Staff.tel_id == dir_id, Staff.check_job.isnot(None))
            )
        )
        result_data = result_data.scalar()
    if result_data is not None:
        return True
    return False


async def check_update_sub(dir_id: int) -> None:
    """
    Функция для подписки на обновления
    :param dir_id: id пользователя в телеграмм
    :return:
    """

    async with get_db_session() as session:
        await session.execute(
            update(Staff).where(Staff.tel_id == dir_id).values(check_job=1)
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
            select(func.count(Staff.id)).where(Staff.check_job.isnot(None))
        )
        result_data = result_data.scalar()
    if result_data >= 1:
        return True
    return False


async def get_busy_empl() -> list:
    """
    Функция для выбора занятых работников
    :return: list
    """

    async with get_db_session() as session:
        result_data = await session.execute(
            select(Staff).where(Staff.check_job.isnot(None))
        )
        result_data = result_data.scalars()
    return [(person.name, person.surname) for person in result_data]


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
            )
            .filter(
                and_(
                    Jobs.time_close.is_(None),
                    Staff.name == name,
                    Staff.surname == surname,
                )
            )
            .order_by(Jobs.id)
        )
        procs = proc_data.unique().scalars().all()
    return [
        (
            proc.id,
            proc.type.job_name,
            proc.company_name,
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
            select(Staff,  func.count(
                    case((Jobs.time_close.is_(None), Jobs.id), else_=None)
                ).label("jobs_count"))
            .options(
                joinedload(Staff.job),
            )
            .outerjoin(Staff.job)
            .where(Staff.check_job.isnot(None))
            .group_by(Staff.id)
            .order_by(Staff.id)
        )
        procs = proc_data.unique().all()
    return [
        (
            staff.name,
            staff.surname,
            job_count,
        )
        for staff, job_count in procs
    ]

async def get_all_data_for_pdf() -> tuple:
    """
    Функция, возвращающая данные по всем сотрудникам для отчета pdf
    :return:
    """
    async with get_db_session() as session:
        all_data = await session.execute(select(Jobs).where(Jobs.time_close.is_(None)).options(
            joinedload(Jobs.staff),
            joinedload(Jobs.type),
        ))
    return all_data.scalars().all()

async def get_personal_data_for_pdf(name: str, surname: str) -> tuple:
    """
    Функция, возвращающая данные по всем определенному сотруднику для отчета pdf
    :return:
    """
    async with get_db_session() as session:
        all_data = await session.execute(select(Jobs).join(Staff).options(
            joinedload(Jobs.type),
            joinedload(Jobs.staff),
        )
        .where(
                and_( Jobs.time_close.is_(None),
                    Staff.name == name,
                    Staff.surname == surname,
                )
            ))
    return all_data.scalars().all()
