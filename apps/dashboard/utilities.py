# Importando bibliotecas do python para mensurar os registros de tempos das equipes:
from datetime import datetime

# Importando modelos para manipulação de dados
from apps.projeto.models import Registro


# Criando as funções do utility

# datas específicas
def get_registros_de_usuario_e_data(equipe, usuario, data):
    registros = Registro.objects.filter(equipe=equipe, criado_por=usuario, criado_em__date=data, eh_registrado=True)

    return sum(registro.minutos for registro in registros)


# Por semanas - Códigos comentados por não estarem funcionais:
# def get_registros_de_equipe_e_semana(equipe, semana):
#     registros = Registro.objects.filter(equipe=equipe, criado_em__month=semana.month, criado_em__week=semana.week, eh_registrado=True)

#     return sum(registro.minutos for registro in registros)


# def get_registros_de_usuario_e_semana(equipe, usuario, semana):
#     registros = Registro.objects.filter(equipe=equipe, criado_por=usuario,   criado_em__month=semana.month, criado_em__week=semana.week, eh_registrado=True)

#     return sum(registro.minutos for registro in registros)


# def get_registros_de_usuario_e_projeto_e_semana(equipe,projeto, usuario, semana):
#     registros = Registro.objects.filter(equipe=equipe, projeto=projeto, criado_por=usuario, criado_em__month=semana.month, criado_em__week=semana.week, eh_registrado=True)

#     return sum(registro.minutos for registro in registros)  


# def get_registros_de_usuario_e_equipe_semana(equipe, usuario, semana):
#     registros = Registro.objects.filter(equipe=equipe, criado_por=usuario, criado_em__month=semana.month, criado_em__week=semana.week, eh_registrado=True)

#     return sum(registro.minutos for registro in registros) 


# Por mês
def get_registros_de_equipe_e_mes(equipe, mes):
    registros = Registro.objects.filter(equipe=equipe, criado_em__year=mes.year, criado_em__month=mes.month, eh_registrado=True)

    return sum(registro.minutos for registro in registros)


def get_registros_de_usuario_e_mes(equipe, usuario, mes):
    registros = Registro.objects.filter(equipe=equipe, criado_por=usuario,   criado_em__year=mes.year, criado_em__month=mes.month, eh_registrado=True)

    return sum(registro.minutos for registro in registros)


def get_registros_de_usuario_e_projeto_e_mes(equipe,projeto, usuario, mes):
    registros = Registro.objects.filter(equipe=equipe, projeto=projeto, criado_por=usuario, criado_em__year=mes.year, criado_em__month=mes.month, eh_registrado=True)

    return sum(registro.minutos for registro in registros)  


def get_registros_de_usuario_e_equipe_e_mes(equipe, usuario, mes):
    registros = Registro.objects.filter(equipe=equipe, criado_por=usuario, criado_em__year=mes.year, criado_em__month=mes.month, eh_registrado=True)

    return sum(registro.minutos for registro in registros) 

