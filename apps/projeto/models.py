from django.db import models
from django.contrib.auth.models import User


# Importando os modelos do app equipe para vincular o projeto a uma equipe
from apps.equipe.models import *


# Criando modelos de Projeto
class Projeto(models.Model):
    equipe = models.ForeignKey(Equipe, related_name='projetos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    criado_por = models.ForeignKey(User, related_name='projetos' , on_delete=models.CASCADE)
    criado_em = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def tempo_registrado(self):
        return sum(registro.minutos for registro in self.registros.all())

    def num_tarefas_pendentes(self):
        return self.tarefas.filter(status=Tarefa.TODO).count() 


class Tarefa(models.Model):

        # Choices de Status:
    TODO = 'todo'
    DONE = 'done'
    ARCHIVED = 'archived'

    CHOICES_STATUS = (
        # (Choice, label)
        (TODO, 'Pendente'),
        (DONE, 'Finalizada'),
        (ARCHIVED, 'Arquivada')
    )

    equipe = models.ForeignKey(Equipe, related_name='tarefas', on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, related_name='tarefas', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    criado_por = models.ForeignKey(User, related_name='tarefas' , on_delete=models.CASCADE)
    criado_em = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=TODO)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome

    def tempo_registrado(self):
        return sum(registro.minutos for registro in self.registros.all())

    
class Registro(models.Model):
    equipe = models.ForeignKey(Equipe, related_name='registros', on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, related_name='registros', on_delete=models.CASCADE, blank=True, null=True)
    tarefa = models.ForeignKey(Tarefa, related_name='registros', on_delete=models.CASCADE, blank=True, null=True)
    minutos = models.IntegerField(default=0)
    eh_registrado = models.BooleanField(default=False)
    criado_por = models.ForeignKey(User, related_name='registros', on_delete=models.CASCADE)
    criado_em = models.DateTimeField()

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        if self.tarefa:
            return '%s - %s' % (self.tarefa.nome, self.criado_em)

        return '%s' % self.criado_em
