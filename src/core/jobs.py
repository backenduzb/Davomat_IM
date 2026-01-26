from django.db import transaction
import os, tempfile
from openpyxl import Workbook
from openpyxl.styles import Alignment
from students.models import Student
from teachers.models import Class
from utils.time import current_time
from utils.upload import upload_document

@transaction.atomic
def export_data_job():
    now_caption = current_time()

    wb = Workbook()
    ws = wb.active
    ws.title = "Davomat"

    ws.merge_cells("A1:E1")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws["A1"] = "Kelmagan o‘quvchilar ro‘yxati"

    headers = ["№", "F.I.SH", "SINF", "SANA", "SABAB"]
    widths = [3, 60, 7, 12, 60]

    for col, (header, width) in enumerate(zip(headers, widths), start=1):
        cell = ws.cell(row=2, column=col, value=header)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.column_dimensions[chr(64 + col)].width = width

    students = Student.objects.exclude(status="Bor")

    row = 3
    for idx, student in enumerate(students, start=1):
        ws.cell(row=row, column=1, value=idx)
        ws.cell(row=row, column=2, value=student.full_name)
        ws.cell(row=row, column=3, value=str(student.class_type.class_name))
        ws.cell(row=row, column=4, value=now_caption)
        ws.cell(row=row, column=5, value=student.sababi or "-")
        row += 1

    tmp = tempfile.NamedTemporaryFile(prefix="davomat_", suffix=".xlsx", delete=False)
    file_name = tmp.name
    tmp.close()

    wb.save(file_name)
    upload_document(document_path=file_name)

    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass

    Student.objects.update(status="Bor", sababi="")
    Class.objects.update(this_updated=False)
