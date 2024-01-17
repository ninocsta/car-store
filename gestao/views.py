import io
from django.http import FileResponse
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from veiculos.models import Veiculo, Fotos, Acessorio, Marca
from gestao.models import Venda, Manutencao, Tipo_Manutencao
from django.shortcuts import redirect
from gestao.forms import VendaForm, ManutencaoForm
from .forms import VeiculoForm
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.utils import timezone
from reportlab.pdfgen import canvas
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import A4, landscape
from django.urls import reverse_lazy
# Create your views here.

@method_decorator(login_required(login_url='login'), name='dispatch')
class Lista_Veiculos(ListView):
    model = Veiculo
    template_name = 'lista_veiculos.html'
    context_object_name = 'veiculos'
    paginate_by = 15  # Defina o número de itens por página aqui
    
    
    def get_queryset(self):
        veiculo = super(Lista_Veiculos, self).get_queryset()
        search = self.request.GET.get('search')
        vendido = self.request.GET.get('vendido')

        if search:
            veiculo = veiculo.filter(modelo__icontains=search)
        if vendido == 'on':
            veiculo = veiculo.filter(vendido=True)
        else:
            veiculo = veiculo.filter(vendido=False)

        return veiculo.order_by('modelo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.Form(self.request.GET)
        return context
    
    
@method_decorator(login_required(login_url='login'), name='dispatch')
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


@method_decorator(login_required(login_url='login'), name='dispatch')
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



def gerar_pdf(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        vendas = Venda.objects.filter(data_venda__range=[start_date, end_date])
    else:
        vendas = Venda.objects.all()
        
    buffer = io.BytesIO()

    # Configurar o tamanho da página e o buffer
    p = canvas.Canvas(buffer, pagesize=landscape(A4))

    # Definir fonte e tamanho
    p.setFont("Helvetica", 12)

    # Adicionar título
    p.drawCentredString(400, 550, "Relatório de Vendas")

    # Definir cabeçalhos da tabela
    headers = ["Data da Venda", "Modelo", "Placa", "Valor da Venda", "Valor da Compra", "Lucro"]

    # Definir a posição inicial para os cabeçalhos
    y = 500
    total = 0
    # Desenhar cabeçalhos da tabela
    for i, header in enumerate(headers):
        p.drawString(10 + i * 130, y, header)

    # Definir a posição inicial para os dados
    y -= 20

    # Desenhar dados na tabela
    for venda in vendas:
        y -= 20
        p.drawString(10, y, str(venda.data_venda))
        p.drawString(140, y, str(venda.veiculo.modelo))
        p.drawString(270, y, str(venda.veiculo.placa))
        p.drawString(400, y, str(f'R${venda.valor_venda}'))
        p.drawString(530, y, str(f'R${venda.veiculo.valor_compra}'))
        p.drawString(660, y, str(f'R${venda.lucro}'))
        p.line(5, y-4, 760, y-4)  # Adjust the start and end x-coordinates as needed
        total +=  venda.lucro
    
    total_text = 'Total de lucro: R$' + str(total)
    text_width = p.stringWidth(total_text, 'Helvetica', 12)  # Calculate the width of the text
    p.drawString(800 - text_width, 20, total_text)  # Subtract the text width from the page width    # Finalizar o PDF
    p.showPage()
    p.save()

    # Redefinir a posição do buffer para o início
    buffer.seek(0)

    # Retornar o arquivo PDF como uma resposta de arquivo
    return FileResponse(buffer, as_attachment=True, filename='vendas.pdf')



@login_required(login_url='login')
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


@method_decorator(login_required(login_url='login'), name='dispatch')
class Lista_Vendas(ListView):
    model = Venda
    template_name = 'lista_vendas.html'
    context_object_name = 'vendas'
    paginate_by = 15


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



class Resumo_Venda(DetailView):
    model = Venda
    template_name = 'resumo_venda.html'
    context_object_name = 'venda'
    success_url = '/area_do_lojista/vendas/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venda = self.get_object()
        context['veiculo'] = venda.veiculo
        context['manutencoes'] = venda.veiculo.veiculo_manutencao.all()
        context ['total_manutencoes'] = venda.veiculo.veiculo_manutencao.all().aggregate(Sum('valor'))['valor__sum'] or 0
    
        return context


class VendaUpdateView(UpdateView):
    model = Venda
    form_class = VendaForm
    template_name = 'editar_venda.html'
    success_url = '/area_do_lojista/vendas/'

    def get_initial(self):
        initial = super().get_initial()
        venda = self.get_object()
        initial['data_venda'] = venda.data_venda.strftime('%Y-%m-%d')
        return initial



    
class VendaDeleteView(DeleteView):
    model = Venda
    success_url = reverse_lazy('lista_vendas')


@method_decorator(login_required(login_url='login'), name='dispatch')
class Lista_Manutencao(ListView):
    model = Manutencao
    template_name = 'lista_manutencoes.html'
    context_object_name = 'manutencoes'
    paginate_by = 15
    
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


class ManutencaoUpdateView(UpdateView):
    model = Manutencao
    form_class = ManutencaoForm
    template_name = 'editar_manutencao.html'
    success_url = '/area_do_lojista/manutencoes/'

    def get_initial(self):
        initial = super().get_initial()
        manutencao = self.get_object()
        initial['data'] = manutencao.data.strftime('%Y-%m-%d')
        return initial



class ManutencaoDeleteView(DeleteView):
    model = Manutencao
    success_url = reverse_lazy('manutencoes')

@login_required(login_url='login')
def nova_manutencao(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    if request.method == 'POST':
        form = ManutencaoForm(request.POST)
        if form.is_valid():
            manutencao = form.save(commit=False)
            manutencao.veiculo = veiculo
            manutencao.save()
            return redirect('manutencoes')
    else:
        form = ManutencaoForm()

    return render(request, 'nova_manutencao.html', {'form': form, 'veiculo': veiculo})


@login_required(login_url='login')
def dashboard(request):
    veiculos = Veiculo.objects.all()
    vendas = Venda.objects.all().order_by('-data_venda')[:5]
    ano_atual = timezone.now().year
    mes_atual = timezone.now().month

    total_vendas_ano = Venda.objects.filter(data_venda__year=ano_atual).count()


    total_vendas_mes = Venda.objects.filter(data_venda__month=mes_atual).aggregate(Sum('valor_venda'))['valor_venda__sum']
    total_vendas_mes = total_vendas_mes if total_vendas_mes is not None else 0

    total_custo_mes = Veiculo.objects.filter(venda_veiculo__data_venda__month=mes_atual).aggregate(Sum('valor_compra'))['valor_compra__sum']
    total_custo_mes = total_custo_mes if total_custo_mes is not None else 0

    total_manutencoes_por_veiculo_vendido_no_mes = Manutencao.objects.filter(veiculo__venda_veiculo__data_venda__month=mes_atual).aggregate(Sum('valor'))['valor__sum']
    total_manutencoes_por_veiculo_vendido_no_mes = total_manutencoes_por_veiculo_vendido_no_mes if total_manutencoes_por_veiculo_vendido_no_mes is not None else 0

    lucro = total_vendas_mes - total_custo_mes - total_manutencoes_por_veiculo_vendido_no_mes










    total_vendidos = veiculos.filter(vendido=True, venda_veiculo__data_venda__month=mes_atual).count()
    total_disponiveis = veiculos.filter(vendido=False).count()
    
    vendas_por_mes = []

    for mes in range(1, 13):
        vendas_mensais = Venda.objects.filter(data_venda__year=ano_atual, data_venda__month=mes)
        total_vendas_mes = vendas_mensais.aggregate(Sum('valor_venda'))['valor_venda__sum'] or 0
        vendas_por_mes.append(total_vendas_mes)

    lucro_por_mes = []

    for mes in range(1, 13):
        vendas_mensais = Venda.objects.filter(data_venda__year=ano_atual, data_venda__month=mes)
        total_vendas_mes = vendas_mensais.aggregate(Sum('valor_venda'))['valor_venda__sum'] or 0
        custo_mensal = Veiculo.objects.filter(venda_veiculo__data_venda__year=ano_atual, venda_veiculo__data_venda__month=mes).aggregate(Sum('valor_compra')) ['valor_compra__sum'] or 0
        manutencoes_mensais = Manutencao.objects.filter(veiculo__venda_veiculo__data_venda__year=ano_atual, veiculo__venda_veiculo__data_venda__month=mes).aggregate(Sum('valor'))['valor__sum'] or 0
        lucro_por_mes.append(total_vendas_mes - custo_mensal - manutencoes_mensais) or 0

    return render(request, 'dashboard.html', {'total_vendas_mes': total_vendas_mes,  'total_vendidos': total_vendidos, 'total_disponiveis': total_disponiveis,  'lucro': lucro, 'lucro_por_mes': lucro_por_mes, 'vendas': vendas, 'total_vendas_ano': total_vendas_ano})




class AcessorioListView(ListView):
    model = Acessorio
    template_name = 'acessorios.html'
    context_object_name = 'acessorios'
    paginate_by = 15

    def get_queryset(self):
        acessorio = super(AcessorioListView, self).get_queryset()
        search = self.request.GET.get('search')

        if search:
            acessorio = acessorio.filter(nome__icontains=search).order_by('nome')
        else:
            acessorio = acessorio.order_by('nome')
        
        return acessorio


class AcessorioCreateView(CreateView):
    model = Acessorio
    fields = ['nome']  # Adicione os campos que você quer editar
    success_url = reverse_lazy('lista_acessorios')


class AcessorioUpdateView(UpdateView):
    model = Acessorio
    fields = ['nome']  # Adicione os campos que você quer editar
    success_url = reverse_lazy('lista_acessorios')


class AcessorioDeleteView(DeleteView):
    model = Acessorio
    success_url = reverse_lazy('lista_acessorios')



class TipoManutencaoListView(ListView):


    model = Tipo_Manutencao
    template_name = 'tipo_manutencao.html'
    context_object_name = 'manutencoes'
    paginate_by = 15

    def get_queryset(self):
        manutencao = super(TipoManutencaoListView, self).get_queryset()
        search = self.request.GET.get('search')

        if search:
            manutencao = manutencao.filter(nome__icontains=search).order_by('nome')
        else:
            manutencao = manutencao.order_by('nome')
        
        return manutencao


class TipoManutencaoCreateView(CreateView):
    model = Tipo_Manutencao
    fields = ['nome']  # Adicione os campos que você quer editar
    success_url = reverse_lazy('lista_tipos_manutencao')


class TipoManutencaoUpdateView(UpdateView):


    model = Tipo_Manutencao
    fields = ['nome']  # Adicione os campos que você quer editar
    success_url = reverse_lazy('lista_tipos_manutencao')


class TipoManutencaoDeleteView(DeleteView):

    model = Tipo_Manutencao
    success_url = reverse_lazy('lista_tipos_manutencao')


class MarcaListView(ListView):
    model = Marca
    template_name = 'marcas.html'
    context_object_name = 'marcas'
    paginate_by = 15

    def get_queryset(self):
        marca = super(MarcaListView, self).get_queryset()
        search = self.request.GET.get('search')

        if search:
            marca = marca.filter(nome__icontains=search).order_by('nome')
        else:
            marca = marca.order_by('marca')
        
        return marca


class MarcaCreateView(CreateView):
    model = Marca
    fields = ['nome']  # Adicione os campos que você quer editar
    success_url = reverse_lazy('lista_marcas')


class MarcaUpdateView(UpdateView):
    model = Marca
    fields = ['nome']  # Adicione os campos que você quer editar
    success_url = reverse_lazy('lista_marcas')


class MarcaDeleteView(DeleteView):
    model = Marca
    success_url = reverse_lazy('lista_marcas')