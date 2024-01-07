from django.shortcuts import render
from django.http.response import HttpResponse
from Usuario.models import CustomUser, GrupoAtendimento
import requests
from xml.etree import ElementTree
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib import messages
from django.shortcuts import redirect
from datetime import date
from datetime import datetime
from django.utils import timezone



def sincronizar_grupos_atendimento(grupos_xml):
    for nome_grupo in grupos_xml:
        try:
            grupo = GrupoAtendimento.objects.get(nome=nome_grupo)
        except GrupoAtendimento.DoesNotExist:
            grupo = GrupoAtendimento(nome=nome_grupo, visivel=True, criado_em=timezone.now(), atualizado_em=timezone.now())
            grupo.save()

def buscar_grupos_atendimento():
    url = "https://selecoes.lais.huol.ufrn.br/media/grupos_atendimento.xml"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Erro ao buscar os dados do XML:", e)
        return []

    tree = ElementTree.fromstring(response.content)

    grupos_atendimento = []

    for grupo in tree.findall('grupoatendimento'):
        visivel = grupo.find('visivel')
        if visivel is not None and visivel.text == 'true':
            nome_grupo = grupo.find('nome').text if grupo.find('nome') is not None else "Desconhecido"
            grupos_atendimento.append(nome_grupo)

    sincronizar_grupos_atendimento(grupos_atendimento)

    print("Grupos de Atendimento finalizados:", grupos_atendimento)
    return grupos_atendimento


def cadastro(request):
    if request.method == "POST":
        cpf = request.POST.get('cpf')
        nome_completo = request.POST.get('nome_completo')
        data_nascimento = request.POST.get('data_nascimento')
        senha = request.POST.get('password')
        teve_covid = request.POST.get('teve_covid_ultimos_30_dias') == 'on'
        senha = request.POST.get('password')
        confirmar_senha = request.POST.get('confirm_password')
        nomes_grupos = request.POST.getlist('grupos_atendimento')
        nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y').date()
        
        userEncontrado = CustomUser.objects.get(cpf=cpf)
        if userEncontrado:
            messages.error(request, 'Já existe um usuário com este cpf')
            return redirect('cadastro')

        idade = (date.today() - nascimento).days / 365.25

        nao_tev_covid_ultimos_30_dias = not teve_covid
        grupos_nao_permitidos = ['População Privada de Liberdade', 'Pessoas Acamadas com mais de 80 anos',
                                 'Pessoas com Deficiência Institucionalizadas','Pessoas ACAMADAS de 80 anos ou mais']
        pertence_grupo_nao_permitido = any(grupo in grupos_nao_permitidos for grupo in nomes_grupos)
        is_apto = idade >= 18 and nao_tev_covid_ultimos_30_dias and not pertence_grupo_nao_permitido
        
        if senha != confirmar_senha:
            messages.error(request, 'A confirmação da senha não corresponde à senha inserida.')
            return redirect('cadastro')

        if idade < 18:
            messages.error(request, 'Usuário deve ser maior de 18 anos.')
            return redirect('cadastro')

        try:
            nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y').date()
            data_nascimento_formatada = nascimento.strftime('%Y-%m-%d')
        except ValueError:
            messages.error(request, 'Formato de data inválido.')
            return redirect('cadastro')

        user = CustomUser.objects.create_user(
            cpf=cpf,
            nome_completo=nome_completo,
            data_nascimento=data_nascimento_formatada,
            password=senha,
            teve_covid_ultimos_30_dias=teve_covid,
            is_apto_agendamento=is_apto
        )
        grupos_objs = []
        for nome_grupo in nomes_grupos:
            try:
                grupo = GrupoAtendimento.objects.get(nome=nome_grupo)
                grupos_objs.append(grupo)
            except GrupoAtendimento.DoesNotExist:
                print(f"Grupo de atendimento não encontrado: {nome_grupo}")
        
        user.grupos_atendimento.set(grupos_objs)

        messages.success(request, 'Usuário cadastrado com sucesso')
        return redirect('login')
    else:
        grupos_atendimento = buscar_grupos_atendimento()
        return render(request, 'cadastro.html', {'grupos_atendimento': grupos_atendimento})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        cpf = request.POST.get('cpf')
        senha = request.POST.get('password')

        user = authenticate(request, cpf=cpf, password=senha)
        
        if user is not None:
            login_django(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')
