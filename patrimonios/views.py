from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Patrimonio
from .forms import PatrimonioForm

def lista_patrimonios(request):
    patrimonios = Patrimonio.objects.all()
    return render(request, 'patrimonios/lista_patrimonios.html', {'patrimonios': patrimonios})

def criar_patrimonio(request):
    if request.method == 'POST':
        form = PatrimonioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patrimônio criado com sucesso!")
            return redirect('patrimonios:lista_patrimonios')
    else:
        form = PatrimonioForm()
    return render(request, 'patrimonios/criar_patrimonio.html', {'form': form})

def detalhar_patrimonio(request, id):
    patrimonio = get_object_or_404(Patrimonio, id=id)
    content_title = f"Detalhes do Patrimônio: {patrimonio.nome}"
    return render(request, 'patrimonios/detalhar_patrimonio.html', {'patrimonio': patrimonio, 'content_title': content_title})

def editar_patrimonio(request, id):
    patrimonio = get_object_or_404(Patrimonio, id=id)
    if request.method == 'POST':
        form = PatrimonioForm(request.POST, instance=patrimonio)
        if form.is_valid():
            form.save()
            messages.success(request, "Patrimônio editado com sucesso!")
            return redirect('patrimonios:lista_patrimonios')
    else:
        form = PatrimonioForm(instance=patrimonio)
    return render(request, 'patrimonios/editar_patrimonio.html', {'form': form, 'patrimonio': patrimonio})

def excluir_patrimonio(request, id):
    patrimonio = get_object_or_404(Patrimonio, id=id)
    if request.method == 'POST':
        patrimonio.delete()
        messages.success(request, "Patrimônio deletado com sucesso!")
        return redirect('patrimonios:lista_patrimonios')
    return render(request, 'patrimonios/lista_patrimonios.html')