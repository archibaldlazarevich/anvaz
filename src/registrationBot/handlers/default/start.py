from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy import insert, select, update

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.registrationBot.middlewares.middlewares import TestMiddleware
from src.database.create_db import get_db_session
from src.database.models import Staff


router_register_start = Router()

router_register_start.message.outer_middleware(TestMiddleware())


class RegisterStaff(StatesGroup):
    init = State()
    surname = State()


@router_register_start.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    async with get_db_session() as session:
        user_data = await session.execute(
            select(Staff).where(Staff.tel_id == message.from_user.id)
        )
        user_data = user_data.scalar()
        if user_data is None:
            await state.set_state(RegisterStaff.init)
            await session.execute(
                insert(Staff).values(tel_id=message.from_user.id, status=1)
            )
            await session.commit()
            await message.reply("Введите свою фамилию")
        elif user_data.status == 4:
            await message.reply("Вам отказано в регистрации!!!")
        else:
            await message.reply(
                "Пользователь с вашим id уже зарегистрирован!!!"
            )


@router_register_start.message(RegisterStaff.init)
async def cmd_surname(message: Message, state: FSMContext) -> None:
    await state.clear()
    if len(message.text) > 1:
        await state.set_state(RegisterStaff.surname)
        async with get_db_session() as session:
            await session.execute(
                update(Staff)
                .where(Staff.tel_id == message.from_user.id)
                .values(surname=message.text.lower())
            )
            await session.commit()
        await message.reply("Введите свое имя")
    else:
        await state.set_state(RegisterStaff.init)
        await message.reply("Пожалуйста, введите свою фамилию корректно")


@router_register_start.message(RegisterStaff.surname)
async def cmd_surname(message: Message, state: FSMContext) -> None:
    await state.clear()
    if len(message.text) > 1:
        async with get_db_session() as session:
            staff_data = await session.execute(
                update(Staff)
                .where(Staff.tel_id == message.from_user.id)
                .values(name=message.text.lower())
                .returning(Staff)
            )
            await session.commit()
            staff_data = staff_data.scalar()
        await message.reply(
            f"Поздравляю, {staff_data.surname.title()} {staff_data.name.title()}, вы зарегистрированы в системе."
        )
    else:
        await state.set_state(RegisterStaff.surname)
        await message.reply("Пожалуйста, введите свое имя корректно")
