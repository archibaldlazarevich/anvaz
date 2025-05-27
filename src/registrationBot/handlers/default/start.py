from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.database.func.data_func import get_empl_if_exist, insert_new_staff
from src.registrationBot.middlewares.middlewares import TestMiddleware


router_register_start = Router()

router_register_start.message.outer_middleware(TestMiddleware())


class RegisterStaff(StatesGroup):
    init = State()
    surname = State()


async def send_data(message: Message, name=True):
    if name:
        await message.reply("Введите своё имя.")
    else:
        await message.reply("Введите свою фамилию")


@router_register_start.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    user_data = await get_empl_if_exist(empl_id=message.from_user.id)
    if user_data:
        await state.set_state(RegisterStaff.init)
        await send_data(message=message, name=False)
    else:
        await message.reply("Пользователь с вашим id уже зарегистрирован!")


@router_register_start.message(RegisterStaff.init)
async def cmd_surname(message: Message, state: FSMContext) -> None:
    if len(message.text) > 1 and len(message.text.split()) == 1:
        await state.set_state(RegisterStaff.surname)
        await state.update_data(surname=message.text.lower())
        await send_data(message=message)
    else:
        await message.reply("Пожалуйста, введите свою фамилию корректно.")


@router_register_start.message(RegisterStaff.surname)
async def cmd_surname(message: Message, state: FSMContext) -> None:
    name = message.text
    if len(name) > 1 and len(name.split()) == 1:
        surname = await state.get_value("surname")
        await insert_new_staff(
            name=name.lower(), surname=surname, empl_id=message.from_user.id
        )
        await message.reply(
            f"Поздравляю, {surname.title()} {name.title()}, вы зарегистрированы в системе."
        )
        await state.clear()
    else:
        await message.reply("Пожалуйста, введите свое имя корректно.")
