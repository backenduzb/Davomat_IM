from django.urls import include, path

from . import views
from .admin import admin_site

urlpatterns = [
    path("dashboard_inf/", views.all_stats_vew, name="dashboard_inf"),
    path("as/", views.student_list_view, name="viv"),
]
