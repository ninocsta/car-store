from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from accounts.views import login_view, logout_view
from veiculos.views import VeiculoList, DadosVeiculoView, home
from gestao.views import gerar_pdf



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', RedirectView.as_view(url='/home')),
    path('home/', home, name='home'),
    path('area_do_lojista/', include('gestao.urls')),
    path('gerar_pdf/', gerar_pdf, name='gerar_pdf'),
    path('veiculos/', VeiculoList.as_view(), name='veiculos'),
    path('veiculos/<int:pk>/', DadosVeiculoView.as_view(), name='dados_veiculo'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)