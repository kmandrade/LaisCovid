from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from .models import Estabelecimento, AgendamentoUsuario, Agendamento
from datetime import datetime
from django.utils import timezone
from django.urls import reverse



@login_required(login_url="/auth/login/")
def home(request):
    usuario = request.user
    estabelecimentos = Estabelecimento.objects.all()
    agendamento_encontrado = AgendamentoUsuario.objects.filter(usuario=usuario, is_active=True)

    tem_agendamento_ativo = False
    for agendamento in agendamento_encontrado:
        if agendamento.status_agendamento != "Expirado":
            tem_agendamento_ativo = True
            break

    dias_semana = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }

    query = request.GET.get('q')
    filtro = request.GET.get('filtro')
    if query:
        if filtro == 'nome':
            estabelecimentos = estabelecimentos.filter(nome_estabelecimento__icontains=query)
        elif filtro == 'cnes':
            estabelecimentos = estabelecimentos.filter(codigo_cnes__icontains=query)

    agendamentos = AgendamentoUsuario.objects.filter(usuario=usuario)
    for agendamento_usuario in agendamentos:
        agendamento = agendamento_usuario.agendamento
        agendamento.expirado = agendamento_usuario.status_agendamento == "Expirado"
        dia_semana_ing = agendamento.data_agendamento.strftime("%A")
        agendamento.dia_semana = dias_semana.get(dia_semana_ing, dia_semana_ing)
    
    context = {
        'user': usuario,
        'estabelecimentos': estabelecimentos,
        'agendamentos_usuario': agendamentos,
        'tem_agendamento_ativo': tem_agendamento_ativo,
    }

    if tem_agendamento_ativo:
        messages.info(request, "Você já possui um agendamento ativo.")

    return render(request, 'home.html', context)


@login_required(login_url="/auth/login/")
def realizar_agendamento(request):
    usuario = request.user
    estabelecimentos = Estabelecimento.objects.all()

    if request.method == 'GET':
        query = request.GET.get('q', '')
        filtro = request.GET.get('filtro', 'nome')
        if filtro == 'nome':
            estabelecimentos = estabelecimentos.filter(nome_estabelecimento__icontains=query)
        elif filtro == 'cnes':
            estabelecimentos = estabelecimentos.filter(codigo_cnes__icontains=query)
    else:
        estabelecimento_id = request.POST.get('estabelecimento')
        data_agendamento_str = request.POST.get('data_agendamento')
        hora_agendamento = request.POST.get('hora_agendamento')

        try:
            data_agendamento = datetime.strptime(data_agendamento_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Formato de data inválido.")
            return redirect('home')

        dia_da_semana = data_agendamento.weekday()

        if data_agendamento < timezone.now().date():
            messages.error(request, "Por favor, selecione uma data futura para o agendamento.")
            return redirect('home')
        
        if dia_da_semana < 2 or dia_da_semana > 5:
            messages.error(request, "Agendamentos são permitidos apenas de quarta a sábado.")
            return redirect('home')

        agendamento, created = Agendamento.objects.get_or_create(
            estabelecimento_id=estabelecimento_id, 
            data_agendamento=data_agendamento, 
            hora_agendamento=hora_agendamento,
            defaults={'vagas_disponiveis': 5} 
        )

        if agendamento.vagas_disponiveis > 0:
            AgendamentoUsuario.objects.filter(usuario=usuario, is_active=True).update(is_active=False)
            AgendamentoUsuario.objects.create(agendamento=agendamento, usuario=usuario, is_active=True)
            agendamento.vagas_disponiveis -= 1
            agendamento.save()
            messages.success(request, "Agendamento realizado com sucesso.")
            return redirect(reverse('home'))
        else:
            messages.error(request, "Não há vagas disponíveis para este horário.")
            return redirect(reverse('home'))

    estabelecimentos = Estabelecimento.objects.all()
    context = {
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

