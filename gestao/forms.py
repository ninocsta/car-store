from django import forms
from veiculos.models import Veiculo, Fotos
from gestao.models import Venda, Manutencao



class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'

class FotosForm(forms.ModelForm):
    model = Fotos
    fields = ('foto',)
    widget = forms.ClearableFileInput(attrs={"allow_multiple_selected": True})    


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = '__all__'
        exclude = ['veiculo']
        widgets = {
            'data_venda': forms.DateInput(attrs={'type': 'date'})            
        }

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = '__all__'
        exclude = ['veiculo']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})            
        }