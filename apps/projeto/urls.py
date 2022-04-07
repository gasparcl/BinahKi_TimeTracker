from django.urls import path


# Importando as views projetos, projeto, edita_projeto
from .views import * 
from .api import *


app_name = 'projeto'

urlpatterns = [
    path('', projetos, name='projetos'),
    path('<int:projeto_id>/', projeto, name='projeto'),
    path('<int:projeto_id>/editar/', edita_projeto, name='edita_projeto'),
    path('<int:projeto_id>/<int:tarefa_id>/', tarefa, name='tarefa'),
    path('<int:projeto_id>/<int:tarefa_id>/editar/', edita_tarefa, name='edita_tarefa'),
    path('<int:projeto_id>/<int:tarefa_id>/<int:registro_id>/editar/', edita_registro, name='edita_registro'),
    path('<int:projeto_id>/<int:tarefa_id>/<int:registro_id>/excluir/', exclui_registro, name='exclui_registro'),
    path('exclui_registro_abandonado/<int:registro_id>/', exclui_registro_abandonado, name='exclui_registro_abandonado'),
    path('adiciona_registro/<int:registro_id>/', adiciona_registro, name='adiciona_registro'),

    # API
    path('api/start_timer/', api_start_timer, name='api_start_timer'),
    path('api/stop_timer/', api_stop_timer, name='api_stop_timer'),
    path('api/discard_timer/', api_discard_timer, name='api_discard_timer'),
    path('api/get_tasks/', api_get_tasks, name='api_get_tasks'),
]