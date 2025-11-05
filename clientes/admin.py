from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'idade', 'ultimo_contato')
    list_filter = ('cidade', 'estado', 'intolerancias')
    search_fields = ('nome', 'email', 'cpf')
    readonly_fields = ('ultimo_contato',)
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'idade', 'cpf', 'email', 'numero')
        }),
        ('Endereço', {
            'fields': ('cep', 'endereco', 'numero_endereco', 'complemento', 'bairro', 'cidade', 'estado')
        }),
        ('Preferências', {
            'fields': ('intolerancias', 'preferencias_alimentares', 'observacoes')
        }),
        ('Sistema', {
            'fields': ('ultimo_contato',)
        }),
    )