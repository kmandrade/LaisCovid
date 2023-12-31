from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from .models import Estabelecimento


@login_required(login_url="/auth/login/")
def home(request):
    query = request.GET.get('q')
    filtro = request.GET.get('filtro')
    estabelecimentos = Estabelecimento.objects.all()

    if query:
        if filtro == 'nome':
            estabelecimentos = estabelecimentos.filter(nome_estabelecimento__icontains=query)
        elif filtro == 'cnes':
            estabelecimentos = estabelecimentos.filter(codigo_cnes__icontains=query)
    return render(request, 'home.html', {
        'user': request.user,
        'estabelecimentos': estabelecimentos if request.user.is_superuser else None
    })

@login_required(login_url="/auth/login/")
def lista_estabelecimentos(request):
    query = request.GET.get('q')
    filtro = request.GET.get('filtro')
    estabelecimentos = Estabelecimento.objects.all()
   
    if query:
        if filtro == 'nome':
            estabelecimentos = estabelecimentos.filter(nome_estabelecimento__icontains=query)
        elif filtro == 'cnes':
            estabelecimentos = estabelecimentos.filter(codigo_cnes__icontains=query)

    return render(request, 'home.html', {
        'user': request.user,
        'estabelecimentos': estabelecimentos
    })

@login_required(login_url="/auth/login/")
def home(request):
    return render(request, 'home.html', {'user': request.user})

@login_required(login_url="/auth/login/")
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Deslogado com sucesso')
    return redirect('login')

