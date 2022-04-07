from django.contrib import admin


# Importando todos os models de projeto para registro no Django admin
from .models import *


# Registrando
admin.site.register(Projeto)
admin.site.register(Tarefa)
admin.site.register(Registro)

