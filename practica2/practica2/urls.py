"""practica2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from practica2.core import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('email/', views.email, name='email'),
    path('registro/', views.registro, name='signup'),
    path('registro/confirmar/<int:token>', views.confirmar_registro, name='confirmar_registro'),
    path('acceso/',auth_views.LoginView.as_view(), name='login'),
    path('salida/',auth_views.LogoutView.as_view(), name='logout'),
    path('post_login_redirect/',views.post_login_redirect, name='post_login_redirect'),
    path('editar_perfil/', views.editar_perfil , name='editar_perfil'),
    path('archivos/',views.archivos , name='archivos'),
    path('archivos/subir_archivo',views.nuevo_archivo , name='subir_archivo'),
    path('archivos/analisis/<int:id>',views.analizar_archivo , name='analizar_archivo'),
    path('archivos/eliminar/<int:id>',views.eliminar_archivo , name='eliminar_archivo'),
    path('archivos/editar/<int:id>',views.editar_archivo , name='editar_archivo'),

    path('retratos/',views.retratos , name='retratos'),
    path('retratos/subir_retrato',views.nuevo_retrato , name='subir_retrato'),
    path('retratos/eliminar/<int:id>',views.eliminar_retrato , name='eliminar_retrato'),


    path('switch_admin/',views.change_admin , name='switch_admin'),
    path('admin/', admin.site.urls),
    path('<str:username>/', views.profile, name='profile'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)