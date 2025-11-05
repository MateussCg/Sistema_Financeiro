from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('listar/', views.listar_clientes, name='listar_clientes'),
    path('visualizar/<int:id>/', views.visualizar_cliente, name='visualizar_cliente'),
    path('editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
]