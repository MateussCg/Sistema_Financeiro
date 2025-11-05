from django.contrib import admin
from .models import Receita, ItemReceita

class ItemReceitaInline(admin.TabularInline):
    model = ItemReceita
    extra = 1

@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade_produzida', 'preco_por_unidade')
    search_fields = ('nome',)
    inlines = [ItemReceitaInline]

@admin.register(ItemReceita)
class ItemReceitaAdmin(admin.ModelAdmin):
    list_display = ('receita', 'ingrediente', 'quantidade')
    list_filter = ('receita', 'ingrediente')
    search_fields = ('receita__nome', 'ingrediente__nome')