from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from accounts.views import login_view, logout_view
from gestao.views import Lista_Veiculos, Editar_Veiculo, vender_veiculo, Cadastrar_Veiculo, Lista_Vendas, Detalhes_Venda, dashboard, Lista_Manutencao, nova_manutencao, Resumo_Venda, gerar_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', RedirectView.as_view(url='/login')),
    path('area_do_lojista/veiculos/', Lista_Veiculos.as_view(), name='lista_veiculos'),
    path('area_do_lojista/editar_veiculo/<int:pk>/', Editar_Veiculo.as_view(), name='editar_veiculo'),
    path('area_do_lojista/vender_veiculo/<int:id>/', vender_veiculo, name='vender_veiculo'),
    path('area_do_lojista/cadastrar_veiculo/', Cadastrar_Veiculo.as_view(), name='cadastrar_veiculo'),
    path('area_do_lojista/vendas/', Lista_Vendas.as_view(), name='lista_vendas'),
    path('area_do_lojista/detalhe_venda/<int:pk>/', Detalhes_Venda.as_view(), name='detalhe_venda'),
    path('area_do_lojista/dashboard/', dashboard, name='dashboard'),
    path('area_do_lojista/manutencoes/', Lista_Manutencao.as_view(), name='manutencoes'),
    path('area_do_lojista/nova_manutencao/<int:id>/', nova_manutencao, name='nova_manutencao'),
    path('area_do_lojista/resumo_venda/<int:pk>/', Resumo_Venda.as_view(), name='resumo_venda'),
    path('area_do_lojista/gerar_pdf/', gerar_pdf, name='gerar_pdf')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)