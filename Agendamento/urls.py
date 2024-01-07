from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('realizar_agendamento/', views.realizar_agendamento, name='realizar_agendamento')
]