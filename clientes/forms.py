from django import forms
from .models import Cliente
from django.core.validators import RegexValidator

class ClienteForm(forms.ModelForm):
    intolerancias = forms.MultipleChoiceField(
        choices=[('Glúten', 'Glúten'), ('Lactose', 'Lactose'), ('Amendoim', 'Amendoim'), ('Nozes', 'Nozes'), ('Ovos', 'Ovos')],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    outra_intolerancia = forms.CharField(max_length=50, required=False, label="Outra Intolerância")

    class Meta:
        model = Cliente
        fields = ['nome', 'idade', 'cpf', 'email', 'numero', 'cep', 'endereco', 'numero_endereco', 'complemento', 'bairro', 'cidade', 'estado', 'preferencias_alimentares', 'observacoes']
        widgets = {
            'idade': forms.NumberInput(attrs={'min': 0}),
            'cpf': forms.TextInput(attrs={'pattern': r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 'placeholder': '000.000.000-00'}),
            'preferencias_alimentares': forms.Textarea(attrs={'rows': 3}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cep'].required = False
        self.fields['endereco'].required = False
        self.fields['numero_endereco'].required = False
        self.fields['complemento'].required = False
        self.fields['bairro'].required = False
        self.fields['cidade'].required = False
        self.fields['estado'].required = False

    def clean(self):
        cleaned_data = super().clean()
        intolerancias = cleaned_data.get('intolerancias', [])
        outra_intolerancia = cleaned_data.get('outra_intolerancia')
        if outra_intolerancia and outra_intolerancia not in intolerancias:
            intolerancias.append(outra_intolerancia)
        cleaned_data['intolerancias'] = intolerancias
        return cleaned_data