# upload/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('export_xlsx/', views.export_xlsx_to_models, name='export_xlsx_to_models'),
    path('set_null_all/', views.set_null_all, name='set_null_all'),
]
