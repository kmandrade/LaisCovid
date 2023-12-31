from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

@login_required(login_url="/auth/login/")
def home(request):
    return render(request, 'home.html', {'user': request.user})

@login_required(login_url="/auth/login/")
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Deslogado com sucesso')
    return redirect('login')

