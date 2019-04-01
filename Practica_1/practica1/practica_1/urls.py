from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('acceso/', views.acceso, name='login'),
    path('<str:user>', views.usuario, name='usuario'),
    path('acceso/actualizar/', views.update_profile, name='actualizar'),
    path('subida_archivos/', views.upload_files, name='files'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)