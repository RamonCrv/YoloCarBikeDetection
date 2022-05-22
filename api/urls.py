from django.urls import path
from django.contrib import admin
from usuarios.views import CriarUsuario, listar_registros

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registrar/', CriarUsuario, name = 'criarUsuario'),
    path('index/', listar_registros.as_view(), name = 'index'),
    
]
