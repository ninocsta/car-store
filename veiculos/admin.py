from django.contrib import admin
from .models import Marca, Acessorio, Veiculo, Fotos
# Register your models here.


class MarcaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome',)
    search_fields = ('nome',)


class AcessorioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome',)
    search_fields = ('nome',)


class FotosInline(admin.TabularInline):
    model = Fotos
    extra = 2

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'placa', 'ano',)
    list_filter = ('modelo', 'vendido',)
    inlines = [FotosInline,]
    

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('vendido',)
        return self.readonly_fields

admin.site.register(Marca, MarcaAdmin)
admin.site.register(Acessorio, AcessorioAdmin)







