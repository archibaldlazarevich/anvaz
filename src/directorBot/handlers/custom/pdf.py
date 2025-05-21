# from aiogram import Router, F
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.types import Message, ReplyKeyboardRemove
#
# from src.database.pdf_func import (
#     generate_pdf_report_for_all_staff,
#     generate_pdf_report_person,
# )
# import src.directorBot.keyboards.reply as rep
#
# router_dir_pdf = Router()
#
#
# class PDF(StatesGroup):
#     init: State = State()
#     empl: State = State()
#
#
# @router_dir_pdf.message(Command("pdf"))
# async def busy_init(message: Message, state: FSMContext):
#     await state.set_state(PDF.init)
#     await message.reply(
#         "Выберите необходимый пункт меню", reply_markup=rep.employee
#     )
#
#
# @router_dir_pdf.message(F.text == "Все сотрудники", PDF.init)
# async def busy_next(message: Message, state: FSMContext):
#     await state.clear()
#     await generate_pdf_report_for_all_staff()
#     await message.reply_document(
#         reply_markup=ReplyKeyboardRemove(), document="staff_all_report.pdf"
#     )
#
#
# @router_dir_pdf.message(F.text == "Определённый сотрудник", PDF.init)
# async def busy_person(message: Message, state: FSMContext):
#     await state.clear()
#     await state.set_state(PDF.empl)
#     await message.reply(
#         "Выберите работника из списка:",
#         reply_markup=await rep.key_busy_employee(),
#     )
#
#
# @router_dir_pdf.message(PDF.empl)
# async def busy_person_answer(message: Message, state: FSMContext):
#     await state.clear()
#     name, surname = message.text.split()
#     await generate_pdf_report_person(
#         name=name.lower(), surname=surname.lower()
#     )
#     await message.reply_document(
#         reply_markup=ReplyKeyboardRemove(), document="staff_spec_report.pdf"
#     )
