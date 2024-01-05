from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from accounts.views import login_view, logout_view
from gestao.views import Lista_Veiculos, Editar_Veiculo, vender_veiculo, Cadastrar_Veiculo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', RedirectView.as_view(url='/login')),
    path('area_do_lojista/veiculos/', Lista_Veiculos.as_view(), name='lista_veiculos'),
    path('area_do_lojista/editar_veiculo/<int:pk>/', Editar_Veiculo.as_view(), name='editar_veiculo'),
    path('area_do_lojista/vender_veiculo/<int:id>/', vender_veiculo, name='vender_veiculo'),
    path('area_do_lojista/cadastrar_veiculo/', Cadastrar_Veiculo.as_view(), name='cadastrar_veiculo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
