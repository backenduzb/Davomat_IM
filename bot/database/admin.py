from asgiref.sync import sync_to_async
@sync_to_async
def get_student_id(full_name: str, class_name: str):
    from teachers.models import Class, ClassName

    class_name_obj = ClassName.objects.get(name=class_name)
    class_ = Class.objects.get(class_name=class_name_obj)
    student = class_.students.get(full_name=full_name)

    return str(student.id)


@sync_to_async
def get_admin_tg_ids():
    from main.models import Admin
    return list(Admin.objects.values_list("telegram_id", flat=True))

@sync_to_async
def get_all_class():
    from teachers.models import ClassName
    return list(ClassName.objects.values_list('name', flat=True))

@sync_to_async
def get_students(class_name: str):
    from teachers.models import Class, ClassName
    print(class_name)
    class_type = ClassName.objects.get(name=class_name)
    classs = Class.objects.get(class_name=class_type)
    print(list(classs.students.values_list('full_name', flat=True)))
    return list(classs.students.values_list('full_name', flat=True))

@sync_to_async
def get_all_no():
    from students.models import Student
    result = {}

    students = Student.objects.values(
        'class_type__class_name__name', 'full_name', 'status', 'sababi'
    )

    for s in students:
        class_name = s['class_type__class_name__name'] 

        if class_name not in result:
            result[class_name] = {
                "reason": [],
                "no_reason": []
            }

        if s['status'] == "Sababli dars qoldirgan":
            result[class_name]['reason'].append({
                "full_name": s['full_name'],
                "status": s['status'],
                "sababi": s['sababi']
            })
        elif s['status'] == "Darsga kelmagan":
            result[class_name]['no_reason'].append({
                "full_name": s['full_name'],
                "status": s['status'],
                "sababi": s['sababi']
            })

    return result
