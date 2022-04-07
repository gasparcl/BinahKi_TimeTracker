from datetime import datetime

from django import template


# Criando uma função para formatar o tempo em horas e minutos:
def formata_tempo(value):
    h, m = divmod(value, 60)
    return '{:d}h{:02d}m'.format(h, m)

register = template.Library()
register.filter('formata_tempo', formata_tempo)