from re import search
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Fotos, Veiculo

# Create your views here.

class VeiculoList(ListView):
    model = Veiculo
    template_name = 'veiculos.html'
    context_object_name = 'veiculos'
    paginate_by = 3
    def get_queryset(self):
        queryset = super(VeiculoList, self).get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            queryset = queryset.filter(modelo__icontains=q)
        return super().get_queryset().filter(vendido=False)


class DadosVeiculoView(DetailView):
    model = Veiculo
    template_name = 'dados_veiculo.html'
    context_object_name = 'veiculo'
    def get_context_data(self, **kwargs):
        context = super(DadosVeiculoView, self).get_context_data(**kwargs)
        context['fotos'] = Fotos.objects.filter(veiculo=self.object)
        return context
    