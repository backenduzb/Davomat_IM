from .models import Student
from main.admin import admin_site
from django.contrib import admin

class StudentsAdmin(admin.ModelAdmin):
    list_display = ['full_name','status','sababi','class_type']
    search_fields = ['full_name']

admin_site.register(Student, StudentsAdmin)