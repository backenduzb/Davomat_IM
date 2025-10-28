from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from .models import Admin
from teachers.models import Class
from django.contrib.auth.models import User
from students.models import Student

class CustomAdminSite(admin.AdminSite):
    site_header = "My Custom Admin"
    site_title = "Admin Panel"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return my_urls + urls

    def dashboard_view(self, request):
        class_stats = []
        total_students = Student.objects.count()
        visited_students = Student.objects.filter(status="Bor").count()

        for cls in Class.objects.all().order_by("class_name"):
            students = Student.objects.filter(class_type=cls)
            total = students.count()
            visited = students.filter(status="Bor").count()
            reason = students.exclude(sababi="").count()
            no_reason = total - visited - reason

            percent = round((visited / total * 100), 1) if total > 0 else 0

            class_stats.append({
                "name": cls.class_name,
                "total": total,
                "visited": visited,
                "reason": reason,
                "no_reason": no_reason,
                "percent": percent,
            })

        student_percent = round((visited_students / total_students * 100), 1) if total_students > 0 else 0

        context = dict(
            self.each_context(request),
            title="Admin Dashboard",
            total_students=total_students,
            visited_students=visited_students,
            student_percent=student_percent,
            class_stats=class_stats,
        )

        return TemplateResponse(request, "dashboard.html", context)


admin_site = CustomAdminSite(name='custom_admin')

class AdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'telegram_id']
    search_fields = ['telegram_id']

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']
    search_fields = ['username', 'first_name', 'last_name']
admin_site.register(Admin, AdminAdmin)
admin_site.register(User)