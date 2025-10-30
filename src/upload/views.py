from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import openpyxl as xl
from django.db import transaction
from teachers.models import Class, ClassName
from students.models import Student


def to_latin(text: str) -> str:
    mapping = {
        "А":"A","а":"a","Б":"B","б":"b","В":"V","в":"v","Г":"G","г":"g",
        "Д":"D","д":"d","Е":"E","е":"e","Ё":"Yo","ё":"yo","Ж":"J","ж":"j",
        "З":"Z","з":"z","И":"I","и":"i","Й":"Y","й":"y","К":"K","к":"k",
        "Л":"L","л":"l","М":"M","м":"m","Н":"N","н":"n","О":"O","о":"o",
        "П":"P","п":"p","Р":"R","р":"r","С":"S","с":"s","Т":"T","т":"t",
        "У":"U","у":"u","Ф":"F","ф":"f","Х":"X","х":"x","Ц":"Ts","ц":"ts",
        "Ч":"Ch","ч":"ch","Ш":"Sh","ш":"sh","Щ":"Sh","щ":"sh","Ъ":"","ъ":"",
        "Ы":"I","ы":"i","Э":"E","э":"e","Ю":"Yu","ю":"yu","Я":"Ya","я":"ya",
        "Ғ":"G‘","ғ":"g‘","Ў":"O‘","ў":"o‘","Қ":"Q","қ":"q","Ҳ":"H","ҳ":"h",
        "’": "'", "‘": "'",
    }
    return ''.join(mapping.get(ch, ch) for ch in text)


@csrf_exempt
@transaction.atomic
def export_xlsx_to_models(request):
    
    if request.method != "POST" or "file" not in request.FILES:
        return JsonResponse({"error": "Fayl yuborilmadi."}, status=400)

    file = request.FILES["file"]

    try:
        wb = xl.load_workbook(file)
        sheet = wb.active
    except Exception as e:
        return JsonResponse({"error": f"Faylni o‘qishda xato: {str(e)}"}, status=400)

    headers = [cell.value for cell in sheet[1]]
    try:
        fish_col = headers.index("I.F.Sh") + 1
        sinf_col = headers.index("Sinf") + 1
    except ValueError:
        return JsonResponse({"error": "Excel faylda 'I.F.Sh' yoki 'Sinf' ustuni topilmadi."}, status=400)

    count = 0
    for row in sheet.iter_rows(min_row=2, values_only=True):
        fish = row[fish_col - 1]
        sinf = row[sinf_col - 1]

        if not fish or not sinf:
            continue

        fish = to_latin(fish.strip().title())
        sinf = str(sinf).strip()

        class_name_obj, _ = ClassName.objects.get_or_create(name=sinf)

        class_obj, _ = Class.objects.get_or_create(
            class_name=class_name_obj,
            defaults={
                "class_teacher_full_name": "Noma’lum",
                "class_teacher_tg_id": "0",
                "this_updated": False
            },
        )

        student_obj, created = Student.objects.get_or_create(
            full_name=fish,
            defaults={"class_type": class_obj}
        )

        if not student_obj.class_type:
            student_obj.class_type = class_obj
            student_obj.save()

        class_obj.students.add(student_obj)
        count += 1

    return JsonResponse({"message": f"{count} ta o‘quvchi muvaffaqiyatli import qilindi ✅"})

@csrf_exempt
@require_POST
def set_null_all(request):
    try:
        from students.models import Student
        from teachers.models import Class

        
        updated_count = Student.objects.update(status="Bor", sababi="")
        
        class_count = Class.objects.update(this_updated=False)
        return JsonResponse({
            "success": True,
            "message": f"{updated_count} ta o'quvchini {class_count}ta sinf bo'sh qilindi ✅"
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)