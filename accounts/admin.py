from django.contrib import admin

from accounts.models import Loja, PerfilUsuario


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'loja')
    search_fields = ('usuario__username', 'loja__nome')
    list_select_related = ('usuario', 'loja')
