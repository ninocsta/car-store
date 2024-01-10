from django import forms
from matplotlib import widgets
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


class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = '__all__'
        exclude = ['veiculo']
