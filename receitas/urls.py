from django.urls import path
from . import views

app_name = 'receitas'

urlpatterns = [
    path('', views.listar_receitas, name='listar_receitas'),
    path('detalhar/<int:pk>/', views.detalhar_receita, name='detalhar_receita'),
    path('criar-ou-editar/<int:pk>/', views.criar_ou_editar_receita, name='criar_ou_editar_receita'),
    path('criar-ou-editar/', views.criar_ou_editar_receita, name='criar_ou_editar_receita'),
    path('deletar/<int:pk>/', views.deletar_receita, name='deletar_receita'),
    path('relatorio/<int:pk>/', views.gerar_relatorio_receita, name='gerar_relatorio_receita'),
]