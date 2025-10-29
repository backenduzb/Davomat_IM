from django.urls import path, include
from main.admin import admin_site  
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin_site.urls),  
    path('', include("main.urls")),    
    path('upload/', include("upload.urls")),  
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  

