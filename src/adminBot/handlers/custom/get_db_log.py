from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile

router_db_log = Router()


@router_db_log.message(Command("get_db_log"))
async def get_db_log(message: Message, state: FSMContext):
    await state.clear()
    file = FSInputFile(path=("base.db"), filename="base.db")
    log_file = FSInputFile(path=(f"output.log"), filename=f"output.log")
    await message.answer_document(
        document=file,
        caption="Текущая база данных.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer_document(
        document=log_file, caption="Текущий файл логов."
    )
