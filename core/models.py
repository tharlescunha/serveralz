from django.db import models

class ConnectedClient(models.Model):
    nome = models.CharField(max_length=100, blank=True, null=True)
    token = models.CharField(max_length=50, unique=True, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.nome
