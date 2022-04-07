# importando bibliotecas do python e django
from datetime import datetime, timezone
from django.shortcuts import get_object_or_404

# importando models
from .models import Registro
from apps.equipe.models import Equipe


# Definindo funções globais
def registro_ativo(request):
    if request.user.is_authenticated:
        if request.user.userprofile.active_team_id:
            equipe = get_object_or_404(Equipe, pk=request.user.userprofile.active_team_id, status=Equipe.ACTIVE)
            registros_nao_rastreados = Registro.objects.filter(equipe=equipe, criado_por=request.user, minutos=0, eh_registrado=False)

            if registros_nao_rastreados:
                registro_ativo = registros_nao_rastreados.first()
                registro_ativo.seconds_since = int((datetime.now(timezone.utc) - registro_ativo.criado_em).total_seconds())

                return {'registro_ativo_segundos': registro_ativo.seconds_since, 'tempo_inicio': registro_ativo.criado_em.isoformat()}

    return {'registro_ativo_segundos': 0, 'tempo_inicio': datetime.now().isoformat()}