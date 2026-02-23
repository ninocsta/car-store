from django.contrib.auth.models import User
from django.db import models


class Loja(models.Model):
    nome = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.nome


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    loja = models.ForeignKey(Loja, on_delete=models.PROTECT, related_name='usuarios', null=True, blank=True)

    def __str__(self):
        return self.usuario.username
