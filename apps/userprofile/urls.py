from django.urls import path
from .views import *


urlpatterns = [
    path('', meu_perfil, name='meu_perfil'),
    path('editar-perfil/', edita_perfil, name='edita_perfil'),
]