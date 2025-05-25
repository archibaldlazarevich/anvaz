from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.func.data_func import (
    check_if_update,
    check_update_sub,
    cancel_update,
)

router_update = Router()


@router_update.message(Command("update"))
async def get_all_model_car(message: Message, state: FSMContext):
    await state.clear()
    if await check_if_update(dir_id=message.from_user.id):
        await message.reply(
            f"Процесс просмотра новых заявок уже запущен.\n"
            f"Для отмены введите команду: \n/cancel",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply(
            f"Новые заявки и обновленные старые заявки будут присылаться "
            f"по мере поступления.\nДля отмены введите команду: \n/cancel",
            reply_markup=ReplyKeyboardRemove(),
        )
        await check_update_sub(dir_id=message.from_user.id)


@router_update.message(Command("cancel"))
async def cancel_get_all_model_car(message: Message, state: FSMContext):
    await state.clear()
    if await check_if_update(dir_id=message.from_user.id):
        await cancel_update(dir_id=message.from_user.id)
        await message.reply(
            "Поступление данных о новых заявках остановлено.\n"
            "Для возобновления введите команду: \n/update",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply(
            "Вы не включили функцию доставки новых и обновленных старых заявок.\n"
            "Для запуска функции введите команду: \n/update",
            reply_markup=ReplyKeyboardRemove(),
        )
        await cancel_update(dir_id=message.from_user.id)
