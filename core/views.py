from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.contrib.auth.models import User
from ingredientes.models import Ingrediente
from fornadas.models import Fornada
from produtos.models import Produto
from django.db.models import F
from patrimonios.models import Patrimonio
from insumos.models import Insumo


def is_gestor(user):
    return user.is_authenticated and hasattr(user, 'perfil') and user.perfil.perfil == 'GESTOR'

@login_required
def dashboard(request):
    ingredientes_alerta = Ingrediente.objects.filter(quantidade_estoque__lte=F('quantidade_minima'))
    ultimas_fornadas = Fornada.objects.order_by('-data_producao')[:5]  # Corrigido para 'data_producao'
    produtos = Produto.objects.all()
    return render(request, 'core/index.html', {
        'ingredientes_alerta': ingredientes_alerta,
        'ultimas_fornadas': ultimas_fornadas,
        'produtos': produtos,
        'content_title': 'Dashboard ERP Padaria',
    })

@login_required
@user_passes_test(is_gestor)
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'core/listar_usuarios.html', {
        'usuarios': usuarios,
        'content_title': 'Lista de Usuários',
    })
    


@login_required
def dashboard_estoques(request):
    context = {
        'ingredientes_count': Ingrediente.objects.count(),
        'patrimonios_count': Patrimonio.objects.count(),
        'insumos_count': Insumo.objects.count(),
        'alertas_count': Ingrediente.objects.filter(quantidade_estoque__lte=F('quantidade_minima')).count() +
                        Insumo.objects.filter(quantidade_estoque__lte=F('quantidade_minima')).count(),
    }
    return render(request, 'core/dashboard_estoques.html', context)