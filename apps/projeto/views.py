from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Importando modelos de Projeto, Tarefa e Equipe
from .models import *
from apps.equipe.models import *


# Importando datetime para formatar datas:
from datetime import datetime 


# Criando views
@login_required
def projetos(request):
    equipe = get_object_or_404(Equipe, pk=request.user.userprofile.active_team_id, status=Equipe.ACTIVE)
    projetos = equipe.projetos.all()

    if request.method == 'POST':
        nome = request.POST.get('nome')

        if nome:
            projeto = Projeto.objects.create(equipe=equipe, nome=nome, criado_por=request.user)

            messages.info(request, 'O projeto foi criado com sucesso!')

            return redirect('projeto:projetos')

    return render(request, 'projeto/projetos.html', {'equipe':equipe, 'projetos':projetos})



@login_required
def projeto(request, projeto_id):
    equipe = get_object_or_404(Equipe, pk=request.user.userprofile.active_team_id, status=Equipe.ACTIVE)
    projeto = get_object_or_404(Projeto, equipe=equipe, pk=projeto_id)

    if request.method == 'POST':
        nome = request.POST.get('nome')

        if nome:
            tarefa = Tarefa.objects.create(equipe=equipe, projeto=projeto, criado_por=request.user, nome=nome)

            messages.info(request, 'A tarefa foi criada com sucesso!')

            return redirect('projeto:projeto', projeto_id=projeto.id)
            
    tarefas_pendentes = projeto.tarefas.filter(status=Tarefa.TODO)
    tarefas_finalizadas = projeto.tarefas.filter(status=Tarefa.DONE)

    return render(request, 'projeto/projeto.html', {'equipe': equipe, 'projeto': projeto, 'tarefas_pendentes': tarefas_pendentes, 'tarefas_finalizadas': tarefas_finalizadas})


@login_required
def edita_projeto(request, projeto_id):
    equipe = get_object_or_404(Equipe, pk=request.user.userprofile.active_team_id, status=Equipe.ACTIVE)
    projeto = get_object_or_404(Projeto, equipe=equipe, pk=projeto_id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        print(nome)
        if nome:
            print(nome)
            projeto.nome = nome
            print(projeto.nome)
            projeto.save()

            messages.info(request, 'O projeto foi editado com sucesso!')

            return redirect('projeto:projeto', projeto_id=projeto.id)

    return render(request, 'projeto/editar_projeto.html', {'equipe': equipe, 'projeto': projeto})


@login_required
def tarefa(request, projeto_id, tarefa_id):
    equipe = get_object_or_404(Equipe, pk=request.user.userprofile.active_team_id, status=Equipe.ACTIVE)
    projeto = get_object_or_404(Projeto, equipe=equipe, pk=projeto_id)
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id, equipe=equipe)

    if request.method == 'POST':
        horas = int(request.POST.get('horas', 0))
        minutos = int(request.POST.get('minutos', 0))
        data = '%s %s' % (request.POST.get('data'), datetime.now().time())
        minutos_total = (horas * 60) + minutos 

        registro = Registro.objects.create(equipe=equipe, projeto=projeto, tarefa=tarefa, minutos=minutos_total, 
        criado_por=request.user, criado_em=data, eh_registrado=True)

    return render(request, 'projeto/tarefa.html', {'equipe': equipe, 'projeto': projeto, 'tarefa': tarefa, 'today': datetime.today()})


@login_required
def edita_tarefa(request, projeto_id, tarefa_id):
    equipe = get_object_or_404(Equipe, pk=request.user.userprofile.active_team_id, status=Equipe.ACTIVE)
    projeto = get_object_or_404(Projeto, equipe=equipe, pk=projeto_id)
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id, equipe=equipe)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        status = request.POST.get('status')

        if nome:
            tarefa.nome = nome
            tarefa.status = status
            tarefa.save()

            messages.info(request, 'A tarefa foi editada com sucesso!')

            return redirect('projeto:tarefa', projeto_id=projeto.id, tarefa_id=tarefa.id)

    return render(request, 'projeto/editar_tarefa.html', {'equipe': equipe, 'projeto': projeto, 'tarefa': tarefa})


@login_required
def edita_registro(request, projeto_id, tarefa_id, registro_id):
    equipe = get_object_or_404(Equipe, pk=request.user.userprofile.active_team_id, status=Equipe.ACTIVE)
    projeto = get_object_or_404(Projeto, equipe=equipe, pk=projeto_id)
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id, equipe=equipe)
    registro = get_object_or_404(Registro, pk=registro_id, equipe=equipe)

    if request.method == 'POST':
        horas = int(request.POST.get('horas', 0))
        minutos = int(request.POST.get('minutos', 0))

        data = '%s %s' % (request.POST.get('data'), datetime.now().time())

        registro.criado_em = data
        registro.minutos = (horas * 60) + minutos 
        registro.save()

        messages.info(request, 'O registro foi editado com sucesso!')

        return redirect('projeto:tarefa', projeto_id=projeto.id, tarefa_id=tarefa.id)

    # divmod divide a primeira variável pelo parâmetro informado(60): O resultado da divisão são as horas e, 
    # se houver resto, são os minutos:
    horas, minutos = divmod(registro.minutos, 60)

    context = {
        'equipe': equipe,
        'projeto': projeto,
        'tarefa': tarefa,
        'registro': registro,
        'horas': horas,
        'minutos': minutos,
    }

    return render(request, 'projeto/editar_registro.html', context)


@login_required
def exclui_registro(request, projeto_id, tarefa_id, registro_id):
    equipe = get_object_or_404(Equipe, pk=request.user.userprofile.active_team_id, status=Equipe.ACTIVE)
    projeto = get_object_or_404(Projeto, equipe=equipe, pk=projeto_id)
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id, equipe=equipe)
    registro = get_object_or_404(Registro, pk=registro_id, equipe=equipe)
    registro.delete()

    messages.info(request, 'O registro foi excluido com sucesso!')

    return redirect('projeto:tarefa', projeto_id=projeto.id, tarefa_id=tarefa.id)



@login_required
def exclui_registro_abandonado(request, registro_id):
    equipe = get_object_or_404(Equipe, pk=request.user.userprofile.active_team_id, status=Equipe.ACTIVE)
    registro = get_object_or_404(Registro, pk=registro_id, equipe=equipe)
    registro.delete()

    messages.info(request, 'O registro foi excluido com sucesso!')

    return redirect('dashboard')


@login_required
def adiciona_registro(request, registro_id):
    equipe = get_object_or_404(Equipe, pk=request.user.userprofile.active_team_id, status=Equipe.ACTIVE)
    registro = get_object_or_404(Registro, pk=registro_id, equipe=equipe)
    projetos = equipe.projetos.all()

    if request.method == 'POST':
        horas = int(request.POST.get('horas', 0))
        minutos = int(request.POST.get('minutos', 0))
        projeto = request.POST.get('projeto')
        tarefa = request.POST.get('tarefa')

        if projeto and tarefa:
            registro.projeto_id = projeto
            registro.tarefa_id = tarefa
            registro.minutos = (horas * 60) + minutos
            registro.criado_em = '%s %s' % (request.POST.get('data'), registro.criado_em.time())
            registro.eh_registrado = True
            registro.save()

            messages.info(request, 'O registro foi adicionado à tarefa')

            return redirect('dashboard')

    horas, minutos = divmod(registro.minutos, 60)

    context = {
        'horas': horas,
        'minutos': minutos,
        'equipe': equipe,
        'projetos': projetos,
        'registro': registro
    }

    return render(request, 'projeto/adiciona_registro.html', context)