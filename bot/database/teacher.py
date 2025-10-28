from asgiref.sync import sync_to_async

@sync_to_async
def get_all_classes():
    from teachers.models import ClassName
    classes = ClassName.objects.all()
    return [str(i.name) for i in classes]

@sync_to_async
def get_all_teachers_id():
    from teachers.models import Class
    return list(Class.objects.values_list("class_teacher_tg_id", flat=True))

@sync_to_async
def get_teacher_information(teacher_id: str):
    from teachers.models import Class
    class_ = Class.objects.get(class_teacher_tg_id=teacher_id)
    return {
        "class_name":class_.class_name,
        "teacher_name":class_.class_teacher_full_name
    }