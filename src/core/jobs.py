from upload.tg_uploader import upload_document
from teachers.models import Class
from openpyxl import Workbook
from openpyxl.styles import Alignment
from students.models import Student
from django.conf import settings
from datetime import datetime
import pytz
import time
import os


def export_data():
    uz_tz = pytz.timezone("Asia/Tashkent")
    now_date = datetime.now(uz_tz)
    now_caption = now_date.strftime("%Y/%m/%d")
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Davomat"

    ws.merge_cells("A1:E1")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws["A1"] = "Kelmagan o‘quvchilar ro‘yxati"

    headers = ["№", "F.I.SH", "SINF", "SANA", "SABAB"]
    widths = [3, 60, 7, 12, 20]

    for col, (header, width) in enumerate(zip(headers, widths), start=1):
        cell = ws.cell(row=2, column=col, value=header)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.column_dimensions[chr(64 + col)].width = width

    students = Student.objects.exclude(status="Bor")

    row_num = 3
    for idx, student in enumerate(students, start=1):
        ws.cell(row=row_num, column=1, value=idx)
        ws.cell(row=row_num, column=2, value=student.full_name)
        ws.cell(row=row_num, column=3, value=str(student.class_type.class_name))
        ws.cell(row=row_num, column=4, value=now_caption)
        ws.cell(row=row_num, column=5, value=student.sababi or "-")
        row_num += 1

    file_name = os.path.join(settings.BASE_DIR, "Davomat.xlsx")

    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass

    time.sleep(3)
    upload_document(document=file_name)
    time.sleep(3)
    updated_count = Student.objects.update(status="Bor", sababi="")
    class_count = Class.objects.update(this_updated=False)
