from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto
from .forms import ProdutoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/lista_produtos.html', {'produtos': produtos})

@login_required
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produtos:lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/form_produto.html', {'form': form})

@login_required
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produtos:lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/form_produto.html', {'form': form})

@login_required
def visualizar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'produtos/visualizar_produto.html', {'produto': produto})

@login_required
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('produtos:lista_produtos')
    return redirect('produtos:lista_produtos')  # Fallback seguro