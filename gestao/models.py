from django.db import models
from django.db.models import Sum
# Create your models here.

class Venda(models.Model):
    id = models.AutoField(primary_key=True)
    veiculo = models.OneToOneField('veiculos.Veiculo', on_delete=models.PROTECT, related_name='venda_veiculo')
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    data_venda = models.DateField()
    comprador = models.CharField(max_length=50, blank=True, null=True)
    contato = models.CharField(max_length=50, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)     

    def __str__(self):
        return self.veiculo.modelo + ' - ' + self.veiculo.placa

    def save(self, *args, **kwargs):
        self.veiculo.vendido = True
        self.veiculo.save()
        super().save(*args, **kwargs)

    @property
    def lucro(self):
        manutencoes = self.veiculo.veiculo_manutencao.all()
        valor_manutencoes = manutencoes.aggregate(Sum('valor'))['valor__sum']
        if valor_manutencoes is None:
            valor_manutencoes = 0
        return self.valor_venda - self.veiculo.valor_compra - valor_manutencoes

class Tipo_Manutencao(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = 'Tipos de Manutenção'

class Manutencao(models.Model):
    id = models.AutoField(primary_key=True)
    veiculo = models.ForeignKey('veiculos.Veiculo', on_delete=models.PROTECT, related_name='veiculo_manutencao')
    tipo = models.ForeignKey('gestao.Tipo_Manutencao', on_delete=models.PROTECT, related_name='tipo_manutencao')
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    data = models.DateField()
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        modelo = self.veiculo.modelo if self.veiculo.modelo else ''
        placa = self.veiculo.placa if self.veiculo.placa else ''
        return modelo + ' - ' + placa

    class Meta:
        verbose_name_plural = 'Manutenções'