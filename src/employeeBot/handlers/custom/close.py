from aiogram import Bot
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from config.config import ECHO_BOT
from src.database.func.data_func import (
    close_task_by_empl,
    get_all_dir_id,
    get_all_dir_id_for_echo,
)
import src.employeeBot.keyboards.reply as rep
from src.database.func.email_func import send_email

router_close_task = Router()

bot = Bot(token=ECHO_BOT)


class CloseTask(StatesGroup):
    init: State = State()


async def send_task(message: Message, state: FSMContext):
    repl_data = await state.get_value("init")
    await message.reply(
        "Выберите заявку, которые требуется закрыть:",
        reply_markup=repl_data[1],
    )


@router_close_task.message(Command("close"))
async def init_close_task(message: Message, state: FSMContext):
    await state.clear()
    repl_mark = await rep.check_task(empl_id=message.from_user.id)
    if repl_mark:
        await state.set_state(CloseTask.init)
        await state.update_data(init=repl_mark)
        await send_task(message=message, state=state)
    else:
        await message.reply(
            "У вас нет активных заявок", reply_markup=ReplyKeyboardRemove()
        )


@router_close_task.message(CloseTask.init)
async def close_task(message: Message, state: FSMContext):
    task_data = await state.get_value("init")
    if message.text in task_data[0]:
        await state.clear()
        task_data = await close_task_by_empl(
            task_id=int(message.text.split()[2])
        )
        await message.reply(
            "Заявка успешно закрыта:\n"
            f"Заявка № {task_data[0]}\n"
            f"Заказчик: {task_data[1].capitalize()}\n"
            f"Адрес объекта: {task_data[2].capitalize()}\n"
            f"Время регистрации заявки {task_data[3]}\n"
            f"Время закрытия заявки {task_data[4]}",
            reply_markup=ReplyKeyboardRemove(),
        )
        text = (
            f"Сотрудник {task_data[5].title()} {task_data[6].title()} закрыл действующую заявку:\n"
            f"Заявка № {task_data[0]}\n"
            f"Заказчик: {task_data[1].capitalize()}\n"
            f"Адрес объекта: {task_data[2].capitalize()}\n"
            f"Время регистрации заявки {task_data[3]}\n"
            f"Время закрытия заявки {task_data[4]}"
        )
        dir_all_id = await get_all_dir_id_for_echo()
        for dir_id in dir_all_id:
            await bot.send_message(
                text=text,
                chat_id=dir_id,
            )
        await send_email(
            subject=f"Сотрудник {task_data[5].title()} {task_data[6].title()}  выполнил заявку № {task_data[0]}",
            message=text,
        )
    else:
        await message.reply(
            "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
        )
        await send_task(message=message, state=state)
