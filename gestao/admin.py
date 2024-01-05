from django.contrib import admin
from .models import Venda, Manutencao, Tipo_Manutencao
from veiculos.models import Veiculo
# Register your models here.


class VendaAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'valor_venda', 'data_venda', 'comprador', 'contato', 'observacoes')
    search_fields = ('veiculo__modelo', 'veiculo__placa', 'comprador')
    list_filter = ('data_venda',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "veiculo":
            kwargs["queryset"] = Veiculo.objects.filter(vendido=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'tipo', 'valor', 'data', 'observacoes')
    search_fields = ('veiculo__modelo', 'veiculo__placa', 'tipo__nome')
    list_filter = ('data',)



class Tipo_ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

admin.site.register(Venda, VendaAdmin)
admin.site.register(Manutencao, ManutencaoAdmin)
admin.site.register(Tipo_Manutencao, Tipo_ManutencaoAdmin)