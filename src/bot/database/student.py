from asgiref.sync import sync_to_async

@sync_to_async
def get_students_by_teacher(telegram_id: str):
    from teachers.models import Class
    
    try:
        class_obj = Class.objects.get(class_teacher_tg_id=telegram_id)
    except Class.DoesNotExist:
        return []
    
    students = class_obj.students.all()
    return [s.full_name for s in students]

@sync_to_async
def get_student_id(full_name: int, teacher_tg: str):
    from teachers.models import Class
    class_ = Class.objects.get(class_teacher_tg_id=teacher_tg)
    stundet = class_.students.get(full_name=full_name)
    return str(stundet.id)

@sync_to_async
def edit_student_no_reason(id: int):
    from students.models import Student
    from teachers.models import Class
    student = Student.objects.get(id=id)
    classs = Class.objects.get(students=student)
    student.status = "Darsga kelmagan"
    classs.this_updated = True
    classs.save()
    student.save()
    
    return "200"

@sync_to_async
def edit_student_reason(id: int, status: str, sababi: str):
    from students.models import Student
    from teachers.models import Class
    student = Student.objects.get(id=id)
    classs = Class.objects.get(students=student)
    student.status = status
    student.sababi = sababi
    classs.this_updated = True
    classs.save()
    student.save()
    
    return "200"

