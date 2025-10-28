from students.models import Student
from teachers.models import Class
from django.http import JsonResponse
from django.shortcuts import redirect, render

def all_stats_vew(reqeust):
    students_count = Student.objects.count()
    reason = Student.objects.filter(status="Sababli dars qoldirgan").count()
    no_reason = Student.objects.filter(status="Darsga kelmagan").count()
    visited = Student.objects.filter(status="Bor").count()

    print(students_count, no_reason, visited, reason)
    return JsonResponse(
        {
            'total': students_count,
            'reason':reason,
            'no_reason':no_reason,
            'visited':visited
        }
    )

def student_list_view(request):
    all_classes = Student.objects.all().order_by('class_type')
    return render(request, 'dashboard.html', {'all_classes': all_classes})
