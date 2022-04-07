from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Importando model de Equipe
from .models import *


# Views
@login_required
def adiciona(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')

        if nome:
            equipe = Equipe.objects.create(nome=nome, criado_por=request.user)
            equipe.membros.add(request.user)
            equipe.save()

            userprofile = request.user.userprofile
            userprofile.active_team_id = equipe.id
            userprofile.save()

            return redirect('meu_perfil')

    return render(request, 'equipe/add.html')


@login_required
def edita(request):
    equipe = get_object_or_404(Equipe, pk=request.user.userprofile.active_team_id, status=Equipe.ACTIVE, membros__in=[request.user])

    if request.method == 'POST':
        nome = request.POST.get('nome')

        if nome:
            equipe.nome = nome
            equipe.save()

            messages.info(request, "As alterações foram salvas")

            return redirect('equipe:equipe', equipe_id=equipe.id)

    return render(request, 'equipe/edit.html', {'equipe':equipe}) 


@login_required
def equipe(request, equipe_id):
    equipe = get_object_or_404(Equipe, pk=equipe_id, status=Equipe.ACTIVE, membros__in=[request.user])

    return render(request, 'equipe/equipe.html', {'equipe': equipe})


@login_required
def ativa_equipe(request, equipe_id):
    equipe = get_object_or_404(Equipe, pk=equipe_id, status=Equipe.ACTIVE, membros__in=[request.user])
    userprofile = request.user.userprofile
    userprofile.active_team_id = equipe_id
    userprofile.save()

    messages.info(request, "A equipe selecionada foi ativada")

    return redirect('equipe:equipe', equipe_id=equipe.id)
