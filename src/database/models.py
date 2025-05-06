import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import Integer, DateTime


class Base(DeclarativeBase):
    pass


class Staff(Base):
    """
    Модель Персонала
    """

    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(primary_key=True)
    tel_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=True)

class JobType(Base):
    """
    Модель типов работ
    """
    __tablename__ = 'job_type'

    id: Mapped[int] = mapped_column(primary_key=True)
    job_name: Mapped[str] = mapped_column(String, nullable=True)


class Jobs(Base):
    """
    Модель заявки
    """

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[str] = mapped_column(ForeignKey('job_type.id'))
    address: Mapped[str] = mapped_column(String, nullable=False)
    time_add: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.today()
    )
    time_close: Mapped[datetime.datetime] = mapped_column(DateTime)


class Change_jobs(Base):
    """
    Модель изменения заявки
    """

    __tablename__ = "change"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("staff.id", ondelete="CASCADE"), nullable=False
    )
    jobs_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False
    )
    job_name_old: Mapped[str] = mapped_column(String, nullable=False)
    job_name_new: Mapped[str] = mapped_column(String, nullable=False)
    time_change: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.today()
    )
    time_init: Mapped[datetime.datetime] = mapped_column(
        ForeignKey("jobs.time_add")
    )


class Admin(Base):
    """
    Модель админа
    """

    __tablename__ = "admin"
    id: Mapped[int] = mapped_column(primary_key=True)
    tel_ad_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True
    )
