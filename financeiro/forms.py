from django import forms
from .models import Venda, Compra, GastoFixo
from produtos.models import Produto
from ingredientes.models import Ingrediente

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['produto', 'quantidade_vendida']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_vendida': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

class CompraForm(forms.ModelForm):
    # Campo para unidade_medida como escolha
    unidade_medida = forms.ChoiceField(
        label='Unidade de Medida',
        choices=Ingrediente.UNIDADES,  # Usa as mesmas escolhas do modelo Ingrediente
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Compra
        fields = ['ingrediente', 'quantidade_comprada', 'valor_unitario', 'unidade_medida']
        widgets = {
            'ingrediente': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_comprada': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Preenche unidade_medida com a unidade do ingrediente selecionado, se existir
        if self.instance.pk and self.instance.ingrediente_id:  # Verifica se é uma instância existente
            self.fields['unidade_medida'].initial = self.instance.ingrediente.unidade_medida
            self.fields['unidade_medida'].widget.attrs['disabled'] = True  # Desativa edição para instâncias existentes
        elif 'ingrediente' in self.data:
            try:
                ingrediente_id = int(self.data.get('ingrediente'))
                ingrediente = Ingrediente.objects.get(id=ingrediente_id)
                self.fields['unidade_medida'].initial = ingrediente.unidade_medida
                self.fields['unidade_medida'].widget.attrs['disabled'] = True  # Desativa edição após seleção
            except (ValueError, Ingrediente.DoesNotExist):
                pass

    def clean(self):
        cleaned_data = super().clean()
        ingrediente = cleaned_data.get('ingrediente')
        unidade_medida = cleaned_data.get('unidade_medida')

        if ingrediente and unidade_medida and unidade_medida != ingrediente.unidade_medida:
            raise forms.ValidationError(
                "A unidade de medida selecionada não corresponde à unidade do ingrediente."
            )
        return cleaned_data

class GastoFixoForm(forms.ModelForm):
    class Meta:
        model = GastoFixo
        fields = ['descricao', 'valor', 'dia_pagamento']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'dia_pagamento': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '31'}),
        }