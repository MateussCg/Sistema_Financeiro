# fornada/forms.py
from django import forms
from .models import Fornada

class FornadaForm(forms.ModelForm):
    quantidade_total_produzida = forms.IntegerField(
        label="Total de Produtos Gerados",
        disabled=True,
        required=False,
        help_text="Calculado como (Quantidade de Execuções × Quantidade por Receita)"
    )

    class Meta:
        model = Fornada
        fields = ['receita', 'quantidade_produzida', 'produto_gerado']
        widgets = {
            'receita': forms.Select(attrs={'class': 'form-control border-0 rounded-pill'}),
            'quantidade_produzida': forms.NumberInput(attrs={'class': 'form-control border-0 rounded-pill', 'min': '1'}),
            'produto_gerado': forms.Select(attrs={'class': 'form-control border-0 rounded-pill', 'disabled': 'disabled'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and hasattr(self.instance, 'receita') and self.instance.receita:
            self.fields['quantidade_produzida'].initial = self.instance.quantidade_produzida
            self.fields['quantidade_total_produzida'].initial = self.instance.quantidade_produzida * self.instance.receita.quantidade_produzida
            if self.instance.produto_gerado:
                self.fields['produto_gerado'].initial = self.instance.produto_gerado.id
        elif 'receita' in self.data:
            receita_id = self.data.get('receita')
            if receita_id:
                from receitas.models import Receita
                receita = Receita.objects.get(pk=receita_id)
                self.fields['quantidade_produzida'].initial = 1
                self.fields['quantidade_total_produzida'].initial = receita.quantidade_produzida

    def clean(self):
        cleaned_data = super().clean()
        receita = cleaned_data.get('receita')
        quantidade_produzida = cleaned_data.get('quantidade_produzida')
        if receita and quantidade_produzida:
            cleaned_data['quantidade_total_produzida'] = receita.quantidade_produzida * quantidade_produzida
        return cleaned_data