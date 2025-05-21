import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
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
    tel_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        # unique=True ## Правка
    )
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    check_job: Mapped[int] = mapped_column(Integer, nullable=True)
    jobs = relationship("Jobs", back_populates="staff")
    change = relationship("ChangeJobs", back_populates="staff")


class JobType(Base):
    """
    Модель типов работ
    """

    __tablename__ = "job_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_name: Mapped[str] = mapped_column(String, nullable=True)
    number_tasks: Mapped[int] = mapped_column(Integer, nullable=True)
    active: Mapped[int] = mapped_column(Integer, nullable=True)
    jobs = relationship("Jobs", back_populates="type")
    change_old = relationship(
        "ChangeJobs",
        foreign_keys="[ChangeJobs.job_id_old]",
        back_populates="job_old",
    )
    change_new = relationship(
        "ChangeJobs",
        foreign_keys="[ChangeJobs.job_id_new]",
        back_populates="job_new",
    )


class Jobs(Base):
    """
    Модель заявки
    """

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee: Mapped[int] = mapped_column(
        ForeignKey("staff.id", ondelete="CASCADE"), nullable=False
    )
    job_id: Mapped[int] = mapped_column(
        ForeignKey("job_type.id"), nullable=True
    )
    company_id: Mapped[int] = mapped_column(
        ForeignKey(
            "company.id",
        ),
        nullable=True,
    )
    address_id: Mapped[int] = mapped_column(
        ForeignKey(
            "address.id",
        ),
        nullable=True,
    )
    time_add: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.today()
    )
    time_close: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=True
    )
    staff = relationship("Staff", back_populates="jobs")
    type = relationship("JobType", back_populates="jobs")
    company = relationship("Company", back_populates="jobs")
    change = relationship(
        "ChangeJobs",
        foreign_keys="[ChangeJobs.jobs_id]",
        back_populates="jobs",
    )
    change_time = relationship(
        "ChangeJobs",
        foreign_keys="[ChangeJobs.time_init]",
        back_populates="jobs_time",
    )
    address = relationship("Address", back_populates="jobs")


class ChangeJobs(Base):
    """
    Модель изменения заявки
    """

    __tablename__ = "change"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("staff.id"), nullable=False
    )
    jobs_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    job_id_old: Mapped[int] = mapped_column(
        ForeignKey("job_type.id"), nullable=False
    )
    job_id_new: Mapped[int] = mapped_column(
        ForeignKey("job_type.id"), nullable=True
    )
    company_old_id: Mapped[int] = mapped_column(
        ForeignKey("company.id"), nullable=False
    )
    company_new_id: Mapped[int] = mapped_column(
        ForeignKey("company.id"), nullable=True
    )
    address_old_id: Mapped[int] = mapped_column(
        ForeignKey("address.id"), nullable=False
    )
    address_new_id: Mapped[int] = mapped_column(
        ForeignKey("address.id"), nullable=True
    )
    time_change: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=True
    )
    time_init: Mapped[datetime.datetime] = mapped_column(
        ForeignKey("jobs.time_add"), nullable=False
    )
    staff = relationship("Staff", back_populates="change")
    jobs = relationship(
        "Jobs", foreign_keys=[jobs_id], back_populates="change"
    )
    jobs_time = relationship(
        "Jobs", foreign_keys=[time_init], back_populates="change_time"
    )
    job_old = relationship(
        "JobType", foreign_keys=[job_id_old], back_populates="change_old"
    )
    job_new = relationship(
        "JobType", foreign_keys=[job_id_new], back_populates="change_new"
    )
    company_old = relationship(
        "Company", foreign_keys=[company_old_id], back_populates="change_old"
    )
    company_new = relationship(
        "Company", foreign_keys=[company_new_id], back_populates="change_new"
    )
    address_old = relationship(
        "Address", foreign_keys=[address_old_id], back_populates="change_old"
    )
    address_new = relationship(
        "Address", foreign_keys=[address_new_id], back_populates="change_new"
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


class Company(Base):
    """
    Модель обслуживаемых компаний
    """

    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(
        String, nullable=False, unique=True
    )
    tasks: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    jobs = relationship("Jobs", back_populates="company")
    change_old = relationship(
        "ChangeJobs",
        foreign_keys="[ChangeJobs.company_old_id]",
        back_populates="company_old",
    )
    change_new = relationship(
        "ChangeJobs",
        foreign_keys="[ChangeJobs.company_new_id]",
        back_populates="company_new",
    )
    address = relationship(
        "Address",
        back_populates="company",
    )


class Address(Base):
    """
    Модель аресов комапний
    """

    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id"), nullable=False
    )
    company = relationship("Company", back_populates="address")
    jobs = relationship("Jobs", back_populates="address")
    change_old = relationship(
        "ChangeJobs",
        foreign_keys="[ChangeJobs.address_old_id]",
        back_populates="address_old",
    )
    change_new = relationship(
        "ChangeJobs",
        foreign_keys="[ChangeJobs.address_new_id]",
        back_populates="address_new",
    )
