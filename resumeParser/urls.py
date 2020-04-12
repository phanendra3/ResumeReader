from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('download', views.exportCSV, name='downloadCSV'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
