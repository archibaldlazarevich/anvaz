import datetime
import os


from fpdf import FPDF

from src.database.data_func import get_all_data_for_pdf, get_personal_data_for_pdf

#
# async def split_text_to_lines(pdf, text, width):
#     # Разбиваем текст на строки, которые влезают в заданную ширину
#     lines = []
#     line = ''
#     for word in text.split():
#         if pdf.get_string_width(line + ' ' + word) < width:
#             if line:
#                 line += ' ' + word
#             else:
#                 line = word
#         else:
#             lines.append(line)
#             line = word
#     lines.append(line)
#     return lines

async def split_text_to_lines(pdf, text, width):
    lines = []
    line = ''
    for char in text:
        if pdf.get_string_width(line + char) < width - 3:
            line += char
        else:
            lines.append(line)
            line = char
    if line:
        lines.append(line)
    return lines


async def create_pdf(job_list, filename="staff_all_report.pdf"):
    pdf = FPDF(orientation='L')
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'src/database/DejaVuLGCSans.ttf', uni=True)
    pdf.set_font('DejaVu', size=9)

    column_weights = [5, 15, 15, 15, 10, 10, 14, 14]
    available_width = 280
    widths = [w * available_width / 100 for w in column_weights]

    headers = [
        "№", "Наименование работ", "Заказчик",
        "Адрес объекта", "Фамилия", "Имя",
        "Время регистрации", "Время выполнения"
    ]

    x_start = pdf.get_x()
    y_start = pdf.get_y()
    for i, (width, header) in enumerate(zip(widths, headers)):
        pdf.set_xy(x_start + sum(widths[:i]), y_start)
        pdf.multi_cell(width, 9, header, border=1, align='C')
    pdf.ln()

    for job in job_list:
        values = [
            str(job.id),
            job.type.job_name or "",
            job.company_name or "",
            job.address or "",
            job.staff.name or "",
            job.staff.surname or "",
            job.time_add.strftime("%H:%M %d.%m.%Y г.") if job.time_add else "",
            job.time_close.strftime("%H:%M %d.%m.%Y г.") if job.time_close else "-"
        ]
        line_height = 6

        # Разбиваем каждую ячейку на строки
        cell_lines = [await split_text_to_lines(pdf, val, w) for val, w in zip(values, widths)]

        max_lines = max(len(lines) for lines in cell_lines)
        row_height = max_lines * line_height

        # Рисуем рамки для всей строки вручную
        x = x_start
        y = pdf.get_y()
        for width in widths:
            pdf.rect(x, y, width, row_height)
            x += width

        # Выводим текст в ячейках
        x = x_start
        for lines, width in zip(cell_lines, widths):
            pdf.set_xy(x, y)
            # Объединяем строки с переносом, чтобы multi_cell корректно отобразил
            text = '\n'.join(lines)
            pdf.multi_cell(width, line_height, text)
            x += width

        pdf.set_y(y + row_height)

    pdf.output(filename)


async def generate_pdf_report_for_all_staff():
    """
    Функция для составления отчета по всем рабтникам
    :return:
    """
    job_list = await get_all_data_for_pdf()
    await create_pdf(job_list)

async def generate_pdf_report_person(name:str, surname:str):
    """
    Функция для состовления отчета по определенному работнику
    :return:
    """

    job_list = await get_personal_data_for_pdf(name=name, surname=surname)
    print('\njob_list', job_list, '\n')
    await create_pdf(job_list, filename="staff_spec_report.pdf")
