from django import forms
from django.forms import inlineformset_factory
from .models import Receita, ItemReceita

class ReceitaForm(forms.ModelForm):
    modo_preparo = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control border-0 rounded-0 py-2'}),
        required=False,
        help_text='Digite cada passo do modo de preparo em uma nova linha.'
    )
    foto = forms.ImageField(
        required=False,
        help_text='Carregue uma foto do prato (opcional).'
    )
    profissional = forms.CharField(
        max_length=100,
        required=False,
        help_text='Nome do profissional responsável (opcional).'
    )
    rendimento = forms.IntegerField(
        min_value=1,
        initial=20,
        help_text='Número de porções produzidas pela receita.'
    )

    class Meta:
        model = Receita
        fields = ['nome', 'descricao', 'quantidade_produzida', 'preco_por_unidade', 'modo_preparo', 'foto', 'profissional', 'rendimento']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control border-0 rounded-0 py-2'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control border-0 rounded-0 py-2'}),
            'quantidade_produzida': forms.NumberInput(attrs={'class': 'form-control border-0 rounded-0 py-2'}),
            'preco_por_unidade': forms.NumberInput(attrs={'class': 'form-control border-0 rounded-0 py-2', 'step': '0.01'}),
        }

class ItemReceitaForm(forms.ModelForm):
    valor_unitario = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label='Valor Unitário (R$)',
        help_text='O valor será preenchido automaticamente com base no ingrediente.'
    )
    fator_correcao = forms.DecimalField(
        max_digits=5,
        decimal_places=3,
        initial=1.000,
        label='Fator Correção',
        help_text='Fator de correção para o peso (padrão: 1.000).'
    )
    quantidade_bruta = forms.FloatField(
        required=False,
        label='Peso Bruto',
        help_text='Peso bruto do ingrediente (opcional).'
    )

    class Meta:
        model = ItemReceita
        fields = ['ingrediente', 'quantidade', 'quantidade_bruta', 'fator_correcao', 'valor_unitario']
        widgets = {
            'ingrediente': forms.Select(attrs={'class': 'form-control border-0 rounded-0 py-2'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control border-0 rounded-0 py-2', 'step': '0.01'}),
            'quantidade_bruta': forms.NumberInput(attrs={'class': 'form-control border-0 rounded-0 py-2', 'step': '0.01'}),
            'fator_correcao': forms.NumberInput(attrs={'class': 'form-control border-0 rounded-0 py-2', 'step': '0.001'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control border-0 rounded-0 py-2', 'step': '0.01', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Só define valor_unitario se o ingrediente já estiver associado e salvo, ou se houver um ingrediente_id no formulário
        if self.instance.pk and hasattr(self.instance, 'ingrediente_id') and self.instance.ingrediente_id:
            self.fields['valor_unitario'].initial = self.instance.ingrediente.preco_unitario
        elif self.data and self.data.get(f'{self.prefix}-ingrediente'):
            ingrediente_id = self.data.get(f'{self.prefix}-ingrediente')
            from ingredientes.models import Ingrediente
            try:
                ingrediente = Ingrediente.objects.get(pk=ingrediente_id)
                self.fields['valor_unitario'].initial = ingrediente.preco_unitario
            except Ingrediente.DoesNotExist:
                self.fields['valor_unitario'].initial = 0.00

# Formset para itens da receita
ItemReceitaFormSet = inlineformset_factory(
    Receita,
    ItemReceita,
    form=ItemReceitaForm,
    extra=1,
    can_delete=True,
    validate_max=True
)