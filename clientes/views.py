from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente
from django import forms
from django.utils import timezone

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'idade', 'cpf', 'email', 'numero', 'cep', 'endereco', 'numero_endereco', 'complemento', 'bairro', 'cidade', 'estado', 'intolerancias', 'preferencias_alimentares', 'observacoes']

@login_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        idade = request.POST['idade']
        cpf = request.POST['cpf']
        email = request.POST['email']
        numero = request.POST['numero']
        cep = request.POST['cep']
        intolerancias = request.POST.getlist('intolerancias')
        if 'outra_intolerancia' in request.POST and request.POST['outra_intolerancia']:
            intolerancias.append(request.POST['outra_intolerancia'])
        preferencias_alimentares = request.POST.get('preferencias_alimentares', '')
        observacoes = request.POST.get('observacoes', '')
        numero_endereco = request.POST.get('numero_endereco', '')
        complemento = request.POST.get('complemento', '')
        endereco = request.POST.get('endereco', '')
        bairro = request.POST.get('bairro', '')
        cidade = request.POST.get('cidade', '')
        estado = request.POST.get('estado', '')

        cliente = Cliente(
            nome=nome,
            idade=idade,
            cpf=cpf,
            email=email,
            numero=numero,
            cep=cep,
            endereco=endereco,
            numero_endereco=numero_endereco,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            intolerancias=intolerancias,
            preferencias_alimentares=preferencias_alimentares,
            observacoes=observacoes,
            ultimo_contato=timezone.now()
        )
        cliente.save()
        messages.success(request, 'Cliente cadastrado com sucesso!')
        return redirect('clientes:cadastrar_cliente')

    return render(request, 'clientes/cadastrar_cliente.html', {
        'intolerancias_comuns': ['Glúten', 'Lactose', 'Amendoim', 'Nozes', 'Ovos'],
        'content_title': 'Cadastrar Cliente',
    })

@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/listar_clientes.html', {
        'clientes': clientes,
        'content_title': 'Lista de Clientes',
    })

@login_required
def visualizar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    # Limpar o número removendo espaços e hífens
    numero_limpo = ''.join(filter(str.isdigit, str(cliente.numero)))
    context = {
        'cliente': cliente,
        'numero_limpo': numero_limpo
    }
    return render(request, 'clientes/visualizar_cliente.html', context)

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('clientes:visualizar_cliente', id=cliente.id)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar_cliente.html', {'form': form, 'content_title': 'Editar Cliente'})

@login_required
def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('clientes:listar_clientes')
    return redirect('clientes:listar_clientes')  # Fallback seguro