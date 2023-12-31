from django.shortcuts import render
from django.http.response import HttpResponse
from Usuario.models import CustomUser
from Usuario.models import GrupoAtendimento
import requests
from xml.etree import ElementTree

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator, has_permission
from rolepermissions.roles import get_user_roles
from datetime import date, timedelta

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

    print("Grupos de Atendimento finalizados:", grupos_atendimento)
    return grupos_atendimento


def cadastro(request):
    if request.method == "POST":
        cpf = request.POST.get('cpf')
        nome_completo = request.POST.get('nome_completo')
        data_nascimento = request.POST.get('data_nascimento')
        senha = request.POST.get('password')
        teve_covid = request.POST.get('teve_covid_ultimos_30_dias') == 'on'
        nomes_grupos = request.POST.getlist('grupos_atendimento')

        # Validações
        hoje = date.today()
        nascimento = date.fromisoformat(data_nascimento)
        idade = (hoje - nascimento).days / 365.25

        if idade < 18:
            messages.error(request, 'Usuário deve ser maior de 18 anos.')
            return redirect('cadastro')

        user = CustomUser.objects.create_user(
            cpf=cpf,
            nome_completo=nome_completo,
            data_nascimento=data_nascimento,
            password=senha,
            teve_covid_ultimos_30_dias=teve_covid,
            nomes_grupos_atendimento=nomes_grupos
        )

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

        user = authenticate(cpf=cpf, password=senha)
        if user:
            login_django(request, user)
            userEncontrado = CustomUser.objects.filter(cpf=request.user.cpf).first()
            roleAdmin = has_permission(userEncontrado, 'SuperAdmin')
            roles = get_user_roles(userEncontrado)
            print("=====================")
            print(userEncontrado.get_idade())
            print("=====================")
            return render(request,'home.html',{'nome_completo': userEncontrado.nome_completo, 'role' : roleAdmin})
        else:
            return HttpResponse('Email ou senha inválidos')

@login_required(login_url="/auth/login/")
def home(request):
        userEncontrado = CustomUser.objects.filter(username=request.user.username).first()
        return render(request,'home.html',{'nomeUsuario': userEncontrado.username})

@login_required(login_url="/auth/login/")
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Deslogado com sucesso')
    return redirect('login')