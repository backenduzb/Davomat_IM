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
def set_class_students_null(class_name: str):
    from teachers.models import Class
    from students.models import Student

    class_ = Class.objects.get(class_name__name=class_name)  
    students = class_.students.all()

    for student in students:
        student.sababi = ""
        student.status = "Bor"  
        student.save()

    class_.this_updated = True
    class_.save()

    return f"{class_name} sinfidagi {students.count()} o‘quvchi yangilandi."


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

    total_students = 0
    total_reason = 0
    total_no_reason = 0

    for s in students:
        total_students += 1
        class_name = s['class_type__class_name__name']

        if class_name not in result:
            result[class_name] = {
                "reason": [],
                "no_reason": [],
                "total": 0
            }

        result[class_name]["total"] += 1

        if s['status'] == "Sababli dars qoldirgan":
            result[class_name]['reason'].append({
                "full_name": s['full_name'],
                "sababi": s['sababi']
            })
            total_reason += 1
        elif s['status'] == "Darsga kelmagan":
            result[class_name]['no_reason'].append({
                "full_name": s['full_name'],
                "sababi": s['sababi']
            })
            total_no_reason += 1
    for class_name, info in result.items():
        total = info["total"]
        absent = len(info["reason"]) + len(info["no_reason"])
        present = total - absent
        result[class_name]["present_percent"] = round((present / total) * 100, 1) if total else 0

    total_absent = total_reason + total_no_reason
    total_present_percent = round(((total_students - total_absent) / total_students) * 100, 1) if total_students else 0

    result["_summary"] = {
        "total_students": total_students,
        "total_reason": total_reason,
        "total_no_reason": total_no_reason,
        "total_absent": total_absent,
        "total_present_percent": total_present_percent
    }

    return result


