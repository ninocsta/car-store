from django.urls import path
from gestao.views import Lista_Veiculos, Editar_Veiculo, vender_veiculo, Cadastrar_Veiculo, Lista_Vendas, dashboard, Lista_Manutencao, nova_manutencao, Resumo_Venda, AcessorioUpdateView, AcessorioDeleteView, AcessorioListView, AcessorioCreateView, VendaUpdateView, VendaDeleteView, ManutencaoUpdateView, ManutencaoDeleteView, TipoManutencaoCreateView, TipoManutencaoListView, TipoManutencaoUpdateView, TipoManutencaoDeleteView, MarcaListView, MarcaCreateView, MarcaUpdateView, MarcaDeleteView


urlpatterns = [   
    path('veiculos/', Lista_Veiculos.as_view(), name='lista_veiculos'),
    path('editar_veiculo/<int:pk>/', Editar_Veiculo.as_view(), name='editar_veiculo'),
    path('vender_veiculo/<int:id>/', vender_veiculo, name='vender_veiculo'),
    path('cadastrar_veiculo/', Cadastrar_Veiculo.as_view(), name='cadastrar_veiculo'),
    path('vendas/', Lista_Vendas.as_view(), name='lista_vendas'),
    path('dashboard/', dashboard, name='dashboard'),
    path('manutencoes/', Lista_Manutencao.as_view(), name='manutencoes'),
    path('nova_manutencao/<int:id>/', nova_manutencao, name='nova_manutencao'),
    path('resumo_venda/<int:pk>/', Resumo_Venda.as_view(), name='resumo_venda'),
    path('acessorio/<int:pk>/editar/', AcessorioUpdateView.as_view(), name='editar_acessorio'),
    path('acessorio/<int:pk>/deletar/', AcessorioDeleteView.as_view(), name='deletar_acessorio'),
    path('acessorio/novo/', AcessorioCreateView.as_view(), name='novo_acessorio'),
    path('cadastros/acessorios/', AcessorioListView.as_view(), name='lista_acessorios'),
    path('vendas/<int:pk>/editar/', VendaUpdateView.as_view(), name='editar_venda'),
    path('vendas/<int:pk>/deletar/', VendaDeleteView.as_view(), name='deletar_venda'),
    path('manutencao/<int:pk>/editar/', ManutencaoUpdateView.as_view(), name='editar_manutencao'),
    path('manutencao/<int:pk>/deletar/', ManutencaoDeleteView.as_view(), name='deletar_manutencao'),
    path('cadastros/tipos_manutencao/', TipoManutencaoListView.as_view(), name='lista_tipos_manutencao'),
    path('cadastros/tipos_manutencao/novo/', TipoManutencaoCreateView.as_view(), name='novo_tipo_manutencao'),
    path('cadastros/tipos_manutencao/<int:pk>/editar/', TipoManutencaoUpdateView.as_view(), name='editar_tipo_manutencao'),
    path('cadastros/tipos_manutencao/<int:pk>/deletar/', TipoManutencaoDeleteView.as_view(), name='deletar_tipo_manutencao'),
    path('cadastros/marcas/', MarcaListView.as_view(), name='lista_marcas'),
    path('cadastros/marcas/novo/', MarcaCreateView.as_view(), name='nova_marca'),
    path('cadastros/marcas/<int:pk>/editar/', MarcaUpdateView.as_view(), name='editar_marca'),
    path('cadastros/marcas/<int:pk>/deletar/', MarcaDeleteView.as_view(), name='deletar_marca'),
]