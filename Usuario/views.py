from django.shortcuts import render
from django.http.response import HttpResponse
from Usuario.models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator, has_permission
from rolepermissions.roles import get_user_roles

# Create your views here.

def cadastro(request):
    
    return HttpResponse('usuario cadastrado com sucesso')
    


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