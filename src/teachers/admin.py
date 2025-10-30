from django.contrib import admin
from .models import Class, ClassName
from main.admin import admin_site

class ClassAdmin(admin.ModelAdmin):
    list_display = ['class_teacher_full_name','class_name','class_teacher_tg_id','this_updated']
    search_fields = [ 'class_teacher_full_name']

class ClassNameAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin_site.register(ClassName, ClassNameAdmin)
admin_site.register(Class, ClassAdmin)
