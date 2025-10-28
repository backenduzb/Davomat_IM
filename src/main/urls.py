from django.urls import path, include
from .admin import admin_site
from . import views

urlpatterns = [
    path('dashboard_inf/', views.all_stats_vew, name="dashboard_inf"),
    path('as/', views.student_list_view, name="viv")
]
