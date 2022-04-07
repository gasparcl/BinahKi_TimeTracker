from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Importando bibliotecas do python para trabalhar com tempo
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta

# Importando modelos de outros apps
from apps.projeto.models import Registro
from apps.equipe.models import Equipe

# Importando as funções de .utilities
from .utilities import *


# Criando as Views
@login_required
def dashboard(request):
    # Verifica se há uma equipe ativa no perfil do usuário
    if not request.user.userprofile.active_team_id:
        return redirect('meu-perfil')

    # Pegar equipe e ajustar as variáveis
    equipe = get_object_or_404(Equipe, pk=request.user.userprofile.active_team_id, status=Equipe.ACTIVE)
    todos_projetos = equipe.projetos.all()
    membros = equipe.membros.all()
    ##


    # Data usuário, paginação
    num_days = int(request.GET.get('num_days', 0))
    data_usuario = datetime.now() - timedelta(days=num_days)
    registros_data = Registro.objects.filter(equipe=equipe, criado_por=request.user, criado_em__date=data_usuario, eh_registrado=True)
    ##


    # mes_usuario, paginação
    num_meses_usuario = int(request.GET.get('num_meses_usuario', 0))
    mes_usuario = datetime.now() - relativedelta(months=num_meses_usuario)

    for projeto in todos_projetos:
        projeto.registros_de_usuario_e_projeto_e_mes = get_registros_de_usuario_e_projeto_e_mes(equipe, projeto, request.user, mes_usuario)
    ##


    # mes_equipe, paginação     
    num_meses_equipe = int(request.GET.get('num_meses_equipe', 0))
    mes_equipe = datetime.now() - relativedelta(months=num_meses_equipe)

    for membro in membros:
        membro.registros_de_usuario_e_equipe_e_mes = get_registros_de_usuario_e_equipe_e_mes(equipe, membro, mes_equipe)


    registros_abandonados = Registro.objects.filter(
        equipe=equipe,
        criado_por=request.user,
        eh_registrado=False
    ).order_by('-criado_em')

    for registro_abandonado in registros_abandonados:
        registro_abandonado.minutes_since = int((datetime.now(timezone.utc) - registro_abandonado.criado_em).total_seconds() / 60)

    # Criando um dicionário de contexto, com todos os dados necessários
    context = {
        'equipe': equipe,
        'todos_projetos': todos_projetos,
        'registros_data': registros_data,
        'registros_abandonados': registros_abandonados,
        'data_usuario': data_usuario,
        'num_days': num_days,
        'membros': membros,
        # 'num_semanas': num_semanas,
        # 'semana_usuario': semana_usuario,
        'num_meses_usuario': num_meses_usuario,
        'mes_usuario': mes_usuario,
        # 'registros_de_usuario_e_semana': get_registros_de_usuario_e_semana(equipe, request.user, semana_usuario),
        'registros_de_usuario_e_mes': get_registros_de_usuario_e_mes(equipe, request.user, mes_usuario),
        'registros_de_usuario_e_data': get_registros_de_usuario_e_data(equipe, request.user, data_usuario),
        'registros_de_equipe_e_mes': get_registros_de_equipe_e_mes(equipe, mes_equipe),
        'num_meses_equipe': num_meses_equipe,
        'mes_equipe': mes_equipe,
        'projetos': todos_projetos[0:4] 
    }

    return render(request, 'dashboard/dashboard.html', context) 



    # semana_usuario, paginação
    # num_semanas = int(request.GET.get('num_semanas', 0))
    # semana_usuario = datetime.now() - relativedelta(weeks=num_semanas)

    # for projeto in todos_projetos:
    #     projeto.registros_de_usuario_e_projeto_e_semana = get_registros_de_usuario_e_projeto_e_semana(equipe, projeto, request.user, semana_usuario)
    # ##