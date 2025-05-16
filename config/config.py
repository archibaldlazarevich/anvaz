import os
from typing import cast

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Переменные окружения не найдены, т.к. отсутствует файл .env")
else:
    load_dotenv()

DATABASE_URL: str = cast(str, os.getenv("DATABASE_URL"))
DIRECTOR_BOT: str = cast(str, os.getenv("DIRECTOR_BOT"))
EMPLOYEE_BOT: str = cast(str, os.getenv("EMPLOYEE_BOT"))
ADMIN_BOT: str = cast(str, os.getenv("ADMIN_BOT"))
REGISTER_BOT: str = cast(str, os.getenv("REGISTER_BOT"))
ECHO_BOT: str = cast(str, os.getenv("ECHO_BOT"))
EMAIL_NAME: str = cast(str, os.getenv("EMAIL_NAME"))
EMAIL_PASSWORD: str = cast(str, os.getenv("EMAIL_PASSWORD"))
RECIPIENT_EMAIL: str = cast(str, os.getenv("RECIPIENT_EMAIL"))

DEFAULT_EMPLOYEE_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Справка"),
    ("create", "Создать заявку на выезд"),
    ("close", "Закрыть выполненную заявку"),
    ("check", "Посмотреть активные завки"),
    ("update", "Редактировать название заявки"),
)

DEFAULT_DIRECTOR_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Справка"),
    ("in_process", "Заявки в процессе работы"),
    ("update", "Получать данные о новых заявках"),
    ("cancel", "Прекратить получение данных о новых заявках"),
    ("employee", "Получить данные о действующих заявках работника"),
    ("busy", "Получить данные о занятых работниках"),
    ("excel", "Получить данные о завках в excel-виде"),
)

DEFAULT_ADMIN_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Справка"),
    ("add_employee", "Добавить работника"),
    ("add_director", "Добавить начальника"),
    ("add_jobs", "Добавить вид работ"),
    ("rm_employee", "Удалить работника"),
    ("rm_director", "Удалить начальника"),
    ("rm_job", "Удалить вид работы"),
    ("dir_list", "Список начальников"),
    ("emp_list", "Список работников"),
    ("non_staff_list", "Список неопределенных пользователей"),
    ("jobs_list", "Список видов работ"),
    ("number_emp", "Количество работников"),
    ("rm_non_staff", "Перевести пользователя в статус неактивного"),
    ("return_non_staff", "Вернуть пользователя из статуса неактивного"),
)

DEFAULT_REGISTER_COMMAND = (("start", "Запустить бота"),)
