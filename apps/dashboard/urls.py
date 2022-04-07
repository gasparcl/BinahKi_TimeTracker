from django.urls import path, include

# Importando as Views
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('projetos/', include('apps.projeto.urls')),
    path('meu-perfil/', include('apps.userprofile.urls')),
    path('meu-perfil/equipe/', include('apps.equipe.urls')), 
]