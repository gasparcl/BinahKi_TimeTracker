# Importando bibliotecas do python e do django
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime, timezone 

# Importando models
from .models import Projeto, Registro
from apps.equipe.models import Equipe


# Criando Views da API
def api_start_timer(request):
    registro = Registro.objects.create(
        equipe_id=request.user.userprofile.active_team_id,
        minutos=0,
        criado_por=request.user,
        eh_registrado=False,
        criado_em=datetime.now()
    )

    return JsonResponse({'success': True})


def api_stop_timer(request):
    registro = Registro.objects.get(
        equipe_id = request.user.userprofile.active_team_id,
        criado_por = request.user,
        minutos = 0,
        eh_registrado = False
    )

    minutos_registrados = int((datetime.now(timezone.utc) - registro.criado_em).total_seconds() / 60)

    if minutos_registrados < 1:
        minutos_registrados = 1

    registro.minutos = minutos_registrados
    registro.eh_registrado = False
    registro.save()

    return JsonResponse({'success': True, 'entryID': registro.id})


def api_discard_timer(request):
    registros = Registro.objects.filter(
        equipe_id = request.user.userprofile.active_team_id,
        criado_por = request.user,
        eh_registrado = False
        ).order_by('-criado_em')

    if registros:
        registro = registros.first()
        registro.delete()

    return JsonResponse({'success': True})


def api_get_tasks(request):
    projeto_id = request.GET.get('projeto_id', '')

    if projeto_id:
        tarefas = []
        equipe = get_object_or_404(equipe, pk=request.user.userprofile.active_team_id, status=Equipe.ACTIVE)
        projeto = get_object_or_404(Projeto, pk=projeto_id, equipe=equipe)

        for tarefa in projeto.tarefas.all():
            obj = {
                'id': tarefa.id,
                'nome': tarefa.nome
            }
            tarefas.append(obj)
    
        return JsonResponse({'success': True, 'tarefas': tarefas})
    
    return JsonResponse({'success': False})
