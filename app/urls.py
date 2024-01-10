from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from accounts.views import login_view, logout_view
from gestao.views import gerar_pdf
from gestao.urls import urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', RedirectView.as_view(url='/login')),
    path('area_do_lojista/', include('gestao.urls')),    
    path('gerar_pdf/', gerar_pdf, name='gerar_pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)