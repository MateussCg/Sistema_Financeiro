from django.shortcuts import render, redirect, get_object_or_404
from .models import Receita, ItemReceita
from .forms import ReceitaForm, ItemReceitaFormSet
from fornadas.models import Fornada
from django.contrib import messages

def listar_receitas(request):
    receitas = Receita.objects.all()
    return render(request, 'receitas/listar_receitas.html', {'receitas': receitas})

def detalhar_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    fornadas = Fornada.objects.filter(receita=receita)
    itens_com_custo = receita.itens.all().select_related('ingrediente')
    total_insumos = sum(item.custo or 0 for item in itens_com_custo)
    custo_por_porcao = total_insumos / receita.rendimento if receita.rendimento else 0

    return render(request, 'receitas/detalhar_receita.html', {
        'content_title': f'Visualizar Receita: {receita.nome}',
        'receita': receita,
        'itens_com_custo': itens_com_custo,
        'total_insumos': total_insumos,
        'fornadas': fornadas,
    })

def criar_ou_editar_receita(request, pk=None):
    receita = get_object_or_404(Receita, pk=pk) if pk else None
    if request.method == 'POST':
        form = ReceitaForm(request.POST, request.FILES, instance=receita)
        formset = ItemReceitaFormSet(request.POST, instance=receita)
        if form.is_valid() and formset.is_valid():
            receita = form.save()
            formset.instance = receita
            formset.save()
            # Recalcular custos após salvar
            itens = receita.itens.all()
            total_insumos = sum(item.custo or 0 for item in itens)
            receita.custo_total = total_insumos
            receita.custo_por_porcao = total_insumos / receita.rendimento if receita.rendimento else 0
            receita.save()
            messages.success(request, f'Receita "{receita.nome}" {"atualizada" if pk else "criada"} com sucesso!')
            return redirect('receitas:detalhar_receita', pk=receita.pk)
    else:
        form = ReceitaForm(instance=receita)
        # Inicializar formset com queryset vazio para novas receitas
        formset = ItemReceitaFormSet(instance=receita, queryset=ItemReceita.objects.none() if not receita else receita.itens.all())
    return render(request, 'receitas/form_receita.html', {
        'form': form,
        'formset': formset,
        'content_title': 'Editar Receita' if receita else 'Criar Receita'
    })

def deletar_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    if request.method == 'POST':
        nome = receita.nome
        receita.delete()
        messages.success(request, f'Receita "{nome}" deletada com sucesso!')
        return redirect('receitas:listar_receitas')
    return render(request, 'receitas/confirmar_delecao.html', {'receita': receita, 'content_title': 'Confirmar Deleção'})

def gerar_relatorio_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    # Lógica de geração de PDF (implemente conforme necessário)
    # Exemplo simplificado:
    from django.http import HttpResponse
    from io import BytesIO
    from reportlab.pdfgen import canvas
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, f"Relatório da Receita: {receita.nome}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')