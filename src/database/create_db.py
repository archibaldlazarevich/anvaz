from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator
from config.config import DATABASE_URL
from src.database.models import (
    Base,
    Admin,
    Staff,
    JobType,
    ChangeJobs,
    Jobs,
    Company,
)
from faker import Faker
import random


fake = Faker()

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool,
)

async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session


async def create_db() -> None:
    admin = Admin(tel_ad_id=434988753)
    users = [
        Staff(
            tel_id=random.randint(434988753, 500000000),
            status=1,
            name=fake.last_name().lower(),
            surname=fake.last_name().lower(),
        )
        for i in range(3)
    ]
    employees = [
        Staff(
            tel_id=random.randint(43498875, 50000000),
            status=2,
            name=fake.first_name().lower(),
            surname=fake.last_name().lower(),
        )
        for i in range(3)
    ]
    directors = [
        Staff(
            tel_id=random.randint(4349887, 5000000),
            status=3,
            name=fake.first_name().lower(),
            surname=fake.last_name().lower(),
            check_job=1,
        )
        for i in range(3)
    ]
    jobs_type = [
        JobType(job_name=fake.text(max_nb_chars=50).lower()) for i in range(3)
    ]
    jobs = [
        Jobs(
            job_id=i,
            company_id=i,
            employee=i + 3,
        )
        for i in range(1, 4)
    ]
    directors.append(
        Staff(
            tel_id=434988753,
            status=3,
            name=fake.first_name().lower(),
            surname=fake.last_name().lower(),
        )
    )

    company = [
        Company(
            company_name=fake.company().lower(),
            address=fake.street_address(),
        )
        for i in range(1, 4)
    ]

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker.begin() as session:
        session.add(admin)
        session.add_all(users)
        session.add_all(employees)
        session.add_all(directors)
        session.add_all(jobs_type)
        session.add_all(jobs)
        session.add_all(company)
        await session.commit()
