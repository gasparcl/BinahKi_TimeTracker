from django.contrib import admin


# Importando model
from .models import *


# Registrando modelo no Django admin
admin.site.register(Userprofile)