from django.contrib import admin
from .models import Compra, GastoFixo, Venda

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('ingrediente', 'quantidade_comprada', 'valor_unitario', 'data_compra')
    list_filter = ('data_compra', 'ingrediente')
    search_fields = ('ingrediente__nome',)
    date_hierarchy = 'data_compra'

@admin.register(GastoFixo)
class GastoFixoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'dia_pagamento')
    list_filter = ('dia_pagamento', 'data')
    search_fields = ('descricao',)
    date_hierarchy = 'data'

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('produto', 'quantidade_vendida', 'valor_total', 'data_venda')
    list_filter = ('data_venda', 'produto')
    search_fields = ('produto__nome',)
    date_hierarchy = 'data_venda'