# Importando a funcionalidade render do Django, para renderizar a página:
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Import models
from .models import Userprofile
from apps.equipe.models import *


# Views

@login_required
def meu_perfil(request):
    equipes = request.user.equipes.exclude(pk=request.user.userprofile.active_team_id)
    return render(request, 'userprofile/myaccount.html', {'equipes': equipes})


@login_required
def edita_perfil(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.username = request.POST.get('email', '')
        request.user.save()

        messages.info(request, 'Perfil editado com sucesso')

        return redirect('meu_perfil')

    return render(request, 'userprofile/edit_profile.html')
