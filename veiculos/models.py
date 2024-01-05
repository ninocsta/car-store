from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
import os
# Create your models here.

class Marca(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Acessorio(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    id = models.AutoField(primary_key=True)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='marca')
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField(blank=True, null=True)
    placa = models.CharField(max_length=8, blank=True, null=True, unique=True)
    cor = models.CharField(max_length=50, blank=True, null=True)
    acessorios = models.ManyToManyField(Acessorio, related_name='acessorios')
    data_insercao = models.DateTimeField(auto_now_add=True)
    km = models.IntegerField(blank=True, null=True)
    vendido = models.BooleanField(default=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    foto_capa = models.ImageField(upload_to='media/', blank=True, null=True)
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    CAMBIO_CHOICES = [
        ('Automático', 'Automático'),
        ('Manual', 'Manual'),
    ]

    cambio = models.CharField(
        max_length=20,
        choices=CAMBIO_CHOICES,
        default='Manual',  # Pode definir o valor padrão se desejar
    )

    DIRECAO_CHOICES = [
        ('Hidráulica', 'Hidráulica'),
        ('Elétrica', 'Elétrica'),
        ('Mecânica', 'Mecânica'),
        # Adicione mais opções conforme necessário
    ]

    direcao = models.CharField(
        max_length=20,
        choices=DIRECAO_CHOICES,
        default='Hidráulica',
    )

    def __str__(self):
        return self.modelo + ' - ' + self.placa



# Função para excluir fisicamente o arquivo da foto quando o objeto Veiculo é excluído
@receiver(pre_delete, sender=Veiculo)
def fotos_delete(sender, instance, **kwargs):
    # Exclui o arquivo da foto do sistema de arquivos
    if instance.foto_capa:
        if os.path.isfile(instance.foto_capa.path):
            os.remove(instance.foto_capa.path)


# Conectar a função de exclusão de fotos ao sinal pre_delete
pre_delete.connect(fotos_delete, sender=Veiculo)


class Fotos(models.Model):
    id = models.AutoField(primary_key=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='veiculo')
    foto = models.ImageField(upload_to='media/', blank=True, null=True)


# Função para excluir fisicamente o arquivo da foto quando o objeto Foto é excluído
@receiver(pre_delete, sender=Fotos)
def fotos_delete(sender, instance, **kwargs):
    # Exclui o arquivo da foto do sistema de arquivos
    if instance.foto:
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)

    
# Conectar a função de exclusão de fotos ao sinal pre_delete
pre_delete.connect(fotos_delete, sender=Fotos)
