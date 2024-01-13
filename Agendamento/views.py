from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from .models import Estabelecimento, AgendamentoUsuario, Agendamento
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models import Min



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
    
    request.session['agendamentos'] = [agendamento.id for agendamento in agendamentos]
    
    context = {
        'user': usuario,
        'estabelecimentos': estabelecimentos,
        'agendamentos_usuario': agendamentos,
        'tem_agendamento_ativo': tem_agendamento_ativo,
        'is_apto_agendamento': usuario.is_apto_agendamento
    }

    if tem_agendamento_ativo:
        messages.info(request, "Você já possui um agendamento ativo.")

    return render(request, 'home.html', context)


@login_required(login_url="/auth/login/")
def realizar_agendamento(request):
    usuario = request.user
    estabelecimentos = Estabelecimento.objects.all()
    
    agendamentos_ativos = AgendamentoUsuario.objects.filter(usuario=usuario, is_active=True)
    tem_agendamento_ativo_nao_expirado = any(
    agendamento.status_agendamento != 'Expirado' for agendamento in agendamentos_ativos)

    if tem_agendamento_ativo_nao_expirado:
        messages.error(request, "Você já possui um agendamento ativo.")
        return redirect('home')

    if request.method == 'POST':
        estabelecimento_id = request.POST.get('estabelecimento')
        data_agendamento_str = request.POST.get('data_agendamento')
        hora_agendamento = request.POST.get('hora_agendamento')

        if not estabelecimento_id:
            print(estabelecimento_id)
            messages.error(request, "Por favor, selecione um estabelecimento válido.")
            return redirect('home')

        try:
            data_agendamento = datetime.strptime(data_agendamento_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Formato de data inválido.")
            return redirect('home')

        dia_da_semana = data_agendamento.weekday()

        if data_agendamento <= timezone.now().date():
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

        if agendamento.vagas_disponiveis > 5:
            messages.error(request, "Limite de agendamentos excedido para este estabelecimento.")
            return redirect(reverse('home'))
        
        if agendamento.vagas_disponiveis > 0:
            agendamentos_ativos = AgendamentoUsuario.objects.filter(usuario=usuario, is_active=True)
            
            for agendamento_usuario in agendamentos_ativos:
                if agendamento_usuario.status_agendamento == 'Expirado':
                    agendamento_usuario.is_active = False
                    agendamento_usuario.save()
           
            novo_agendamento_usuario = AgendamentoUsuario.objects.create(agendamento=agendamento, usuario=usuario, is_active=True)
            agendamento.vagas_disponiveis -= 1
            agendamento.save()
            messages.success(request, "Agendamento realizado com sucesso.")
            return redirect(reverse('home'))
        else:
            messages.error(request, "Não há vagas disponíveis para este horário.")
            return redirect(reverse('home'))
        
    agendamentos_ids = request.session.get('agendamentos', [])
    
    agendamentos_usuario = AgendamentoUsuario.objects.filter(id__in=agendamentos_ids)
    context = {
        'estabelecimentos': estabelecimentos,
        'agendamentos_usuario': agendamentos_usuario
    }
    
    return render(request, 'home.html', context)

@login_required(login_url="/auth/login/")
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Deslogado com sucesso')
    return redirect('login')

@login_required(login_url="/auth/login/")
def verificar_vagas(request, estabelecimento_id):
    try:
        estabelecimento = Estabelecimento.objects.get(id=estabelecimento_id)
        resultado_agregacao = Agendamento.objects.filter(
            estabelecimento=estabelecimento
        ).aggregate(Min('vagas_disponiveis'))

        vagas_disponiveis = resultado_agregacao['vagas_disponiveis__min']
        if vagas_disponiveis is None:
            vagas_disponiveis = 5

        return JsonResponse({'vagas_disponiveis': vagas_disponiveis})
    except Estabelecimento.DoesNotExist:
        return JsonResponse({'error': 'Estabelecimento não encontrado'}, status=404)
