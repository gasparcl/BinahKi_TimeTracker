from django.db import models
from django.contrib.auth.models import User


# Models
class Equipe(models.Model):
    
    # Status
    ACTIVE = 'active'
    DELETED = 'deleted'

    CHOICES_STATUS = (
        (ACTIVE, 'Ativa'),
        (DELETED, 'Deletada')
    )

    
    # Fields
    nome = models.CharField(max_length=255)
    membros = models.ManyToManyField(User, related_name='equipes')
    criado_por = models.ForeignKey(User, related_name='equipes_criadas', on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)


    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome 

