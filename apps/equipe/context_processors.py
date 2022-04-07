# Importando o model Equipe
from .models import *


# Criando a função de equipe ativa, para definir em qual equipe o membro irá mensurar a tarefa
def equipe_ativa(request):
    if request.user.is_authenticated:
        if request.user.userprofile.active_team_id:
            equipe = Equipe.objects.get(pk=request.user.userprofile.active_team_id)

            return {'equipe_ativa': equipe}
            
    return {'equipe_ativa': None}
