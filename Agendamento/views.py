from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from .models import Estabelecimento, AgendamentoUsuario, Agendamento
from datetime import datetime
from django.shortcuts import get_object_or_404



@login_required(login_url="/auth/login/")
def home(request):
    usuario = request.user
    estabelecimentos = Estabelecimento.objects.all()
    print("========")
    # Processamento do filtro
    query = request.GET.get('q')
    filtro = request.GET.get('filtro')
    if query:
        if filtro == 'nome':
            estabelecimentos = estabelecimentos.filter(nome_estabelecimento__icontains=query)
        elif filtro == 'cnes':
            estabelecimentos = estabelecimentos.filter(codigo_cnes__icontains=query)

    selected_estabelecimento_id = request.GET.get('estabelecimento_id')
    agendamentos = []
    if selected_estabelecimento_id:
        agendamentos = Agendamento.objects.filter(estabelecimento_id=selected_estabelecimento_id)
        for agendamento in agendamentos:
            agendamento.disponivel = not AgendamentoUsuario.objects.filter(agendamento=agendamento, is_active=True).exists()

    context = {
        'user': usuario,
        'estabelecimentos': estabelecimentos,
        'agendamentos': agendamentos,
        'selected_estabelecimento_id': int(selected_estabelecimento_id) if selected_estabelecimento_id else None
    }

    return render(request, 'home.html', context)


@login_required(login_url="/auth/login/")
def realizar_agendamento(request, agendamento_id=None):
    usuario = request.user

    if AgendamentoUsuario.objects.filter(usuario=usuario, is_active=True).exists():
        messages.error(request, "Você já possui um agendamento ativo.")
        return redirect('home')

    agendamento_direto = None
    if agendamento_id:
        agendamento_direto = get_object_or_404(Agendamento, id=agendamento_id)

    if request.method == 'POST' or agendamento_direto:
        agendamento = agendamento_direto

        if not agendamento:
            estabelecimento_id = request.POST.get('estabelecimento')
            data_agendamento = request.POST.get('data_agendamento')
            hora_agendamento = request.POST.get('hora_agendamento')
            agendamento, created = Agendamento.objects.get_or_create(
                estabelecimento_id=estabelecimento_id, 
                data_agendamento=data_agendamento, 
                hora_agendamento=hora_agendamento,
                defaults={'vagas_disponiveis': 5}  # Valor padrão para vagas disponíveis
            )

        if agendamento.vagas_disponiveis > 0:
            AgendamentoUsuario.objects.create(agendamento=agendamento, usuario=usuario, is_active=True)
            agendamento.vagas_disponiveis -= 1
            agendamento.save()
            messages.success(request, "Agendamento realizado com sucesso.")
            return redirect('home')
        else:
            messages.error(request, "Não há vagas disponíveis para este horário.")

    estabelecimentos = Estabelecimento.objects.all()
    context = {
        'agendamento_direto': agendamento_direto,
        'estabelecimentos': estabelecimentos,
    }

    return render(request, 'home.html', context)


@login_required(login_url="/auth/login/")
def lista_agendamento(request):
    query = request.GET.get('q', '')
    filtro = request.GET.get('filtro', 'nome')

    if filtro == 'cnes':
        agendamentos = AgendamentoUsuario.objects.filter(agendamento__estabelecimento__codigo_cnes__icontains=query)
    else:
        agendamentos = AgendamentoUsuario.objects.filter(agendamento__estabelecimento__nome_estabelecimento__icontains=query)

    for agendamento in agendamentos:
        agendamento.expirado = datetime.now() > datetime.combine(agendamento.agendamento.data_agendamento, agendamento.agendamento.hora_agendamento)

    context = {
        'agendamentos': agendamentos
    }
    return render(request, 'home.html', context)

@login_required(login_url="/auth/login/")
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Deslogado com sucesso')
    return redirect('login')

