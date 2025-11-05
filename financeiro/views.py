from django.shortcuts import render, redirect, get_object_or_404
from .models import Venda, Compra, GastoFixo
from produtos.models import Produto
from .forms import VendaForm, CompraForm, GastoFixoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F
from django.core.exceptions import ValidationError

@login_required
def dashboard_financeiro(request):
    total_vendas = Venda.objects.aggregate(total=Sum('valor_total'))['total'] or 0
    total_compras = Compra.objects.aggregate(total=Sum(F('quantidade_comprada') * F('valor_unitario')))['total'] or 0
    total_gastos_fixos = GastoFixo.objects.aggregate(total=Sum('valor'))['total'] or 0
    saldo_caixa = total_vendas - (total_compras + total_gastos_fixos)
    
    # Dados para as tabelas com totais calculados na view
    gastos_fixos = GastoFixo.objects.all()
    total_gastos_fixos_tabela = sum(gasto.valor for gasto in gastos_fixos) if gastos_fixos else 0
    
    compras = Compra.objects.all()
    compras_com_totais = [
        {
            'ingrediente': compra.ingrediente.nome,
            'quantidade': compra.quantidade_comprada,
            'valor_unitario': compra.valor_unitario,
            'total': compra.quantidade_comprada * compra.valor_unitario,
            'data': compra.data_compra,
            'pk': compra.pk
        }
        for compra in compras
    ]
    total_compras_tabela = sum(compra.quantidade_comprada * compra.valor_unitario for compra in compras) if compras else 0
    
    return render(request, 'financeiro/dashboard.html', {
        'total_vendas': total_vendas,
        'total_compras': total_compras,
        'total_gastos_fixos': total_gastos_fixos,
        'saldo_caixa': saldo_caixa,
        'gastos_fixos': gastos_fixos,
        'total_gastos_fixos_tabela': total_gastos_fixos_tabela,
        'compras_com_totais': compras_com_totais,
        'total_compras_tabela': total_compras_tabela,
    })

@login_required
def criar_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            try:
                venda.save()
                messages.success(request, f'Venda de {venda.quantidade_vendida} {venda.produto.nome}(s) registrada!')
                return redirect('financeiro:dashboard_financeiro')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = VendaForm()
    return render(request, 'financeiro/form_venda.html', {'form': form})

@login_required
def criar_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Compra cadastrada com sucesso!")
                return redirect('financeiro:dashboard_financeiro')
            except ValidationError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Erro ao salvar a compra: {str(e)}")
    else:
        form = CompraForm()
    return render(request, 'financeiro/form_compra.html', {'form': form})

@login_required
def criar_gasto_fixo(request):
    if request.method == 'POST':
        form = GastoFixoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Gasto "{form.cleaned_data["descricao"]}" registrado!')
            return redirect('financeiro:dashboard_financeiro')
    else:
        form = GastoFixoForm()
    return render(request, 'financeiro/form_gasto_fixo.html', {'form': form})

@login_required
def historico_transacoes(request):
    vendas = Venda.objects.all().order_by('-data_venda')
    compras = Compra.objects.all().order_by('-data_compra')
    return render(request, 'financeiro/historico_transacoes.html', {
        'vendas': vendas,
        'compras': compras,
    })

@login_required
def editar_gasto(request, pk):
    gasto = get_object_or_404(GastoFixo, pk=pk)
    if request.method == 'POST':
        form = GastoFixoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            messages.success(request, f"Gasto '{gasto.descricao}' atualizado com sucesso!")
            return redirect('financeiro:dashboard_financeiro')
    else:
        form = GastoFixoForm(instance=gasto)
    return render(request, 'financeiro/form_gasto_fixo.html', {'form': form, 'gasto': gasto})

@login_required
def deletar_gasto(request, pk):
    gasto = get_object_or_404(GastoFixo, pk=pk)
    if request.method == 'POST':
        gasto.delete()
        messages.success(request, f"Gasto '{gasto.descricao}' deletado com sucesso!")
        return redirect('financeiro:dashboard_financeiro')
    return redirect('financeiro:dashboard_financeiro')  # Renderiza página de confirmação

@login_required
def detalhes_compra(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    return render(request, 'financeiro/detalhes_compra.html', {'compra': compra})