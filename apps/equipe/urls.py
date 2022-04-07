from django.urls import path
# Importando as views adiciona, equipe, edita e ativa_equipe:
from .views import *


app_name = 'equipe'


urlpatterns = [
    path('adicionar/', adiciona, name='adiciona'),
    path('<int:equipe_id>/', equipe, name='equipe'),
    path('editar/', edita, name='edita'),
    path('ativar_equipe/<int:equipe_id>/', ativa_equipe, name='ativa_equipe'),    
]
