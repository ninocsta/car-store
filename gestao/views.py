from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView
from veiculos.models import Veiculo, Fotos
from gestao.models import Venda, Manutencao
from django.shortcuts import redirect
from gestao.forms import VendaForm
from .forms import VeiculoForm
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.utils import timezone
# Create your views here.


class Lista_Veiculos(ListView):
    model = Veiculo
    template_name = 'lista_veiculos.html'
    context_object_name = 'veiculos'
    paginate_by = 10  # Defina o número de itens por página aqui

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


class Lista_Vendas(ListView):
    model = Venda
    template_name = 'lista_vendas.html'
    context_object_name = 'vendas'
    paginate_by = 20
    
    def get_queryset(self):
        venda = super(Lista_Vendas, self).get_queryset()
        search = self.request.GET.get('search')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if search and start_date and end_date:
            venda = venda.filter(veiculo__modelo__icontains=search, data_venda__range=[start_date, end_date]).order_by('-data_venda')
        elif search and start_date:
            venda = venda.filter(veiculo__modelo__icontains=search, data_venda__gte=start_date).order_by('-data_venda')
        elif search and end_date:
            venda = venda.filter(veiculo__modelo__icontains=search, data_venda__lte=end_date).order_by('-data_venda')
        elif start_date and end_date:
            venda = venda.filter(data_venda__range=[start_date, end_date]).order_by('-data_venda')
        elif search:
            venda = venda.filter(veiculo__modelo__icontains=search).order_by('-data_venda')
        elif start_date:
            venda = venda.filter(data_venda__gte=start_date).order_by('-data_venda')
        elif end_date:
            venda = venda.filter(data_venda__lte=end_date).order_by('-data_venda')
        else:
            venda = venda.order_by('-data_venda')
        
        return venda
    
class Detalhes_Venda(UpdateView):
    model = Venda
    form_class = VendaForm
    template_name = 'detalhe_venda.html'
    success_url = '/area_do_lojista/vendas/'


class Lista_Manutencao(ListView):
    model = Manutencao
    template_name = 'lista_manutencoes.html'
    context_object_name = 'manutencoes'
    paginate_by = 20
    
    def get_queryset(self):
        manutencao = super(Lista_Manutencao, self).get_queryset()
        search = self.request.GET.get('search')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date') 

        if search and start_date and end_date:
            manutencao = manutencao.filter(veiculo__modelo__icontains=search, data__range=[start_date, end_date]).order_by('-data')
        elif search and start_date:
            manutencao = manutencao.filter(veiculo__modelo__icontains=search, data__gte=start_date).order_by('-data')
        elif search and end_date:
            manutencao = manutencao.filter(veiculo__modelo__icontains=search, data__lte=end_date).order_by('-data')
        elif start_date and end_date:
            manutencao = manutencao.filter(data__range=[start_date, end_date]).order_by('-data')
        elif search:
            manutencao = manutencao.filter(veiculo__modelo__icontains=search).order_by('-data')
        elif start_date:
            manutencao = manutencao.filter(data__gte=start_date).order_by('-data')
        elif end_date:
            manutencao = manutencao.filter(data__lte=end_date).order_by('-data')
        else:
            manutencao = manutencao.order_by('-data')
        
        return manutencao


def dashboard(request):
    veiculos = Veiculo.objects.all()
    vendas = Venda.objects.all().order_by('-data_venda')[:5]
    ano_atual = timezone.now().year
    mes_atual = timezone.now().month
    total_vendas_mes = Venda.objects.filter(data_venda__month=mes_atual).aggregate(Sum('valor_venda'))


    total_custo_mes = Veiculo.objects.filter(venda_veiculo__data_venda__month=mes_atual).aggregate(Sum('valor_compra'))
    total_manutencoes_por_veiculo_vendido_no_mes = Manutencao.objects.filter(veiculo__venda_veiculo__data_venda__month=mes_atual).aggregate(Sum('valor'))
    lucro = total_vendas_mes['valor_venda__sum'] - total_custo_mes['valor_compra__sum'] - total_manutencoes_por_veiculo_vendido_no_mes['valor__sum'] 
    total_vendidos = veiculos.filter(vendido=True, venda_veiculo__data_venda__month=mes_atual).count()
    total_disponiveis = veiculos.filter(vendido=False).count()

    custo_mes_veiculo = Veiculo.objects.filter(venda_veiculo__data_venda__month=mes_atual)



    
    vendas_por_mes = []

    for mes in range(1, 13):
        vendas_mensais = Venda.objects.filter(data_venda__year=ano_atual, data_venda__month=mes)
        total_vendas_mes = vendas_mensais.aggregate(Sum('valor_venda'))['valor_venda__sum'] or 0
        vendas_por_mes.append(total_vendas_mes)

    lucro_por_mes = []

    for mes in range(1, 13):
        vendas_mensais = Venda.objects.filter(data_venda__year=ano_atual, data_venda__month=mes)
        total_vendas_mes = vendas_mensais.aggregate(Sum('valor_venda'))['valor_venda__sum'] or 0
        custo_mensal = Veiculo.objects.filter(venda_veiculo__data_venda__year=ano_atual, venda_veiculo__data_venda__month=mes).aggregate(Sum('valor_compra'))['valor_compra__sum'] or 0
        manutencoes_mensais = Manutencao.objects.filter(veiculo__venda_veiculo__data_venda__year=ano_atual, veiculo__venda_veiculo__data_venda__month=mes).aggregate(Sum('valor'))['valor__sum'] or 0
        lucro_por_mes.append(total_vendas_mes - custo_mensal - manutencoes_mensais)

    return render(request, 'dashboard.html', {'total_vendas_mes': total_vendas_mes,  'total_vendidos': total_vendidos, 'total_disponiveis': total_disponiveis,  'lucro': lucro, 'lucro_por_mes': lucro_por_mes, 'vendas': vendas})

