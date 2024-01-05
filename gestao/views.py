from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView
from veiculos.models import Veiculo, Fotos
from gestao.models import Venda
from django.shortcuts import redirect
from gestao.forms import VendaForm
from .forms import VeiculoForm
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
# Create your views here.


class Lista_Veiculos(ListView):
    model = Veiculo
    template_name = 'lista_veiculos.html'
    context_object_name = 'veiculos'
    def get_queryset(self):
        veiculo = super(Lista_Veiculos, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            veiculo = veiculo.filter(modelo__icontains=search).order_by('modelo')
        return veiculo
    

class Editar_Veiculo(UpdateView):
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'editar_veiculo.html'
    success_url = '/area_do_lojista/veiculos/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['fotos'] = PhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['fotos'] = PhotoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        fotos = context['fotos']
        self.object = form.save()
        if fotos.is_valid():
            fotos.instance = self.object
            fotos.save()
        return super().form_valid(form)

PhotoFormSet = inlineformset_factory(Veiculo, Fotos, fields=('foto',), extra=3, can_delete=True)

class Cadastrar_Veiculo(CreateView):
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'cadastrar_veiculo.html'
    success_url = '/area_do_lojista/veiculos/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['fotos'] = PhotoFormSet(self.request.POST, self.request.FILES)
        else:
            data['fotos'] = PhotoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        fotos = context['fotos']
        self.object = form.save()
        if fotos.is_valid():
            fotos.instance = self.object
            fotos.save()
        return super().form_valid(form)

def vender_veiculo(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            venda.veiculo = veiculo
            venda.save()
            return redirect('lista_veiculos')
    else:
        form = VendaForm()
    return render(request, 'vender_veiculo.html', {'form': form, 'veiculo': veiculo})