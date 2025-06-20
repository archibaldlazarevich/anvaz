import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault


# adminbot
from src.adminBot.handlers.default.start import router_start_admin
from src.adminBot.handlers.default.help import router_help_admin

from src.adminBot.handlers.custom.add_address import router_add_address
from src.adminBot.handlers.custom.add_company import router_add_company
from src.adminBot.handlers.custom.address_list import router_address_list
from src.adminBot.handlers.custom.company_list import router_company_list
from src.adminBot.handlers.custom.get_db_log import router_db_log
from src.adminBot.handlers.custom.return_address import router_return_address
from src.adminBot.handlers.custom.return_company import router_return_company
from src.adminBot.handlers.custom.rm_address import router_address_rm
from src.adminBot.handlers.custom.rm_company import router_company_rm
from src.adminBot.handlers.custom.return_job import router_return_job
from src.adminBot.handlers.custom.add_director import router_add_directors
from src.adminBot.handlers.custom.add_employee import router_add_empl
from src.adminBot.handlers.custom.add_jobs import router_add_jobs
from src.adminBot.handlers.custom.directors_list import router_dir_list
from src.adminBot.handlers.custom.employee_list import router_emp_list
from src.adminBot.handlers.custom.jobs_list import router_jobs_list
from src.adminBot.handlers.custom.non_staff_list import router_non_staff_list
from src.adminBot.handlers.custom.number_employee import router_emp_number
from src.adminBot.handlers.custom.rm_director import router_rm_directors
from src.adminBot.handlers.custom.rm_employee import router_rm_employee
from src.adminBot.handlers.custom.rm_job import router_rm_jobs
from src.adminBot.handlers.custom.rm_non_employee import router_rm_non_staff
from src.adminBot.handlers.custom.ban_non_empl_list import (
    router_ban_non_empl_list,
)
from src.adminBot.handlers.custom.return_non_employee import (
    router_return_non_staff,
)
from src.adminBot.middlewares.middlewares import AdminAccessMiddleware
from src.database.func.data_func import get_admin_id

# dir bot

from src.directorBot.handlers.custom.change_empl import router_change
from src.directorBot.handlers.custom.exel_change import router_dir_excel_change
from src.directorBot.handlers.custom.job_number import router_dir_job_number
from src.directorBot.handlers.default.start import router_start_dir
from src.directorBot.handlers.default.help import router_help_dir
from src.directorBot.handlers.custom.in_process import router_in_process
from src.directorBot.handlers.custom.employee import router_dir_emp
from src.directorBot.handlers.custom.excel import router_dir_excel
from src.directorBot.handlers.custom.update_cancel import router_update
from src.directorBot.handlers.custom.busy import router_dir_busy_emp

from src.database.func.data_func import get_all_dir_id
from src.directorBot.middlewares.middlewares import DirectorAccessMiddleware

# employee bot

from src.database.func.data_func import get_all_empl_id
from src.employeeBot.handlers.default.start import router_empl_start
from src.employeeBot.handlers.default.help import router_empl_help
from src.employeeBot.handlers.custom.close import router_close_task
from src.employeeBot.handlers.custom.update import router_update_task
from src.employeeBot.handlers.custom.check import router_check_task
from src.employeeBot.handlers.custom.create import router_create_task

from src.employeeBot.middlewares.middlewares import EmployeeAccessMiddleware

# registration_bot

from src.registrationBot.handlers.default.start import router_register_start

## all_bot_data
from config.config import (
    ADMIN_BOT,
    DEFAULT_ADMIN_COMMANDS,
    DIRECTOR_BOT,
    DEFAULT_DIRECTOR_COMMANDS,
    EMPLOYEE_BOT,
    DEFAULT_EMPLOYEE_COMMANDS,
    REGISTER_BOT,
    DEFAULT_REGISTER_COMMAND,
    ECHO_BOT,
)


bot_admin = Bot(
    token=ADMIN_BOT,
)
bot_dir = Bot(
    token=DIRECTOR_BOT,
)
bot_register = Bot(
    token=REGISTER_BOT,
)
bot_employee = Bot(
    token=EMPLOYEE_BOT,
)
bot_echo = Bot(
    token=ECHO_BOT,
)


dp_admin = Dispatcher()
dp_dir = Dispatcher()
dp_register = Dispatcher()
dp_employee = Dispatcher()
dp_echo = Dispatcher()


async def set_commands_admin():
    commands_admin = [
        BotCommand(command=command[0], description=command[1])
        for command in DEFAULT_ADMIN_COMMANDS
    ]
    await bot_admin.set_my_commands(commands_admin, BotCommandScopeDefault())


async def set_commands_dir():
    commands_dir = [
        BotCommand(command=command[0], description=command[1])
        for command in DEFAULT_DIRECTOR_COMMANDS
    ]
    await bot_dir.set_my_commands(commands_dir, BotCommandScopeDefault())


async def set_commands_register():
    commands_register = [
        BotCommand(command=command[0], description=command[1])
        for command in DEFAULT_REGISTER_COMMAND
    ]
    await bot_register.set_my_commands(
        commands_register, BotCommandScopeDefault()
    )


async def set_commands_empl():
    commands_employee = [
        BotCommand(command=command[0], description=command[1])
        for command in DEFAULT_EMPLOYEE_COMMANDS
    ]
    await bot_employee.set_my_commands(
        commands_employee, BotCommandScopeDefault()
    )


async def start_bot_admin():
    dp_admin.include_routers(
        router_help_admin,
        router_start_admin,
        router_add_directors,
        router_add_empl,
        router_add_jobs,
        router_dir_list,
        router_emp_list,
        router_jobs_list,
        router_non_staff_list,
        router_emp_number,
        router_rm_directors,
        router_rm_employee,
        router_rm_jobs,
        router_rm_non_staff,
        router_return_non_staff,
        router_ban_non_empl_list,
        router_return_job,
        router_add_address,
        router_add_company,
        router_company_list,
        router_address_list,
        router_return_address,
        router_return_company,
        router_address_rm,
        router_company_rm,
        router_db_log,
    )
    dp_admin.startup.register(set_commands_admin)
    dp_admin.message.middleware(
        AdminAccessMiddleware(get_allowed_ids=get_admin_id)
    )
    await bot_admin.delete_webhook(drop_pending_updates=True)
    await bot_admin.set_my_description(
        "Admin Bot — мощный административный инструмент "
        "для управления базой данных. "
        "Добавляйте и удаляйте компании,"
        " сотрудников, адреса и виды работ, "
        "контролируйте списки пользователей и "
        "получайте отчёты о состоянии системы.",
        language_code="ru",
    )
    await dp_admin.start_polling(
        bot_admin, allowed_updates=dp_admin.resolve_used_update_types()
    )


async def start_bot_dir():
    dp_dir.include_routers(
        router_help_dir,
        router_start_dir,
        router_in_process,
        router_update,
        router_dir_busy_emp,
        router_dir_emp,
        router_dir_excel,
        router_change,
        router_dir_excel_change,
        router_dir_job_number,
    )
    dp_dir.startup.register(set_commands_dir)
    dp_dir.message.middleware(
        DirectorAccessMiddleware(get_allowed_ids=get_all_dir_id)
    )
    await bot_dir.delete_webhook(drop_pending_updates=True)
    await bot_dir.set_my_description(
        "Director Bot — инструмент для руководителей, "
        "который помогает контролировать процесс работы. "
        "Просматривайте заявки в работе, получайте "
        "актуальные данные по сотрудникам, "
        "распределяйте задачи и анализируйте занятость команды.",
        language_code="ru",
    )
    await dp_dir.start_polling(
        bot_dir, allowed_updates=dp_dir.resolve_used_update_types()
    )


async def start_bot_register():
    dp_register.include_routers(
        router_register_start,
    )
    dp_register.startup.register(set_commands_register)
    await bot_register.delete_webhook(drop_pending_updates=True)
    await bot_register.set_my_description(
        "Register Bot — простой и безопасный бот для регистрации новых "
        "сотрудников в системе. Обеспечивает быстрый ввод данных и интеграцию"
        " с базой, позволяя легко расширять команду.",
        language_code="ru",
    )
    await dp_register.start_polling(
        bot_register, allowed_updates=dp_register.resolve_used_update_types()
    )


async def start_bot_empl():
    dp_employee.include_routers(
        router_empl_help,
        router_create_task,
        router_close_task,
        router_update_task,
        router_check_task,
        router_empl_start,
    )
    dp_employee.startup.register(set_commands_empl)
    dp_employee.message.middleware(
        EmployeeAccessMiddleware(get_allowed_ids=get_all_empl_id)
    )

    await bot_employee.delete_webhook(drop_pending_updates=True)
    await bot_employee.set_my_description(
        "Employee Bot — удобный помощник для сотрудников. "
        "Позволяет быстро создавать, просматривать, редактировать "
        "и закрывать заявки на выезд. Всегда под рукой для "
        "оперативного взаимодействия с задачами.",
        language_code="ru",
    )
    await dp_employee.start_polling(
        bot_employee, allowed_updates=dp_employee.resolve_used_update_types()
    )


async def start_bot_echo():
    await bot_echo.delete_webhook(drop_pending_updates=True)
    await bot_echo.set_my_description(
        "Echo Bot — централизованный бот для рассылки уведомлений "
        "и сообщений, которые генерируются другими вашими ботами "
        "(сотрудников, руководителей, администраторов и регистрации). "
        "Он автоматически доставляет важную информацию подписчикам без "
        "необходимости ввода команд, обеспечивая оперативное информирование "
        "и синхронизацию данных между всеми участниками системы.",
        language_code="ru",
    )
    await dp_echo.start_polling(
        bot_echo, allowed_updates=dp_echo.resolve_used_update_types()
    )


async def main():
    tasks = [
        asyncio.create_task(start_bot_admin()),
        asyncio.create_task(start_bot_dir()),
        asyncio.create_task(start_bot_register()),
        asyncio.create_task(start_bot_empl()),
        asyncio.create_task(start_bot_echo()),
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
