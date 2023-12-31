from django.contrib import admin
from .models import Estabelecimento, Agendamento, AgendamentoUsuario
from django.urls import path
from django.shortcuts import render
from django.db.models import Count

@admin.register(Estabelecimento)
class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ('nome_estabelecimento', 'codigo_cnes')
    search_fields = ['nome_estabelecimento', 'codigo_cnes']

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_filter = ('estabelecimento', 'data_agendamento',)
    list_display = ('estabelecimento', 'data_agendamento',)
    search_fields = ('estabelecimento', 'data_agendamento',)
    ordering = ('estabelecimento', 'data_agendamento',)
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('graficos/', self.admin_site.admin_view(self.grafico_view), name='agendamento-graficos'),
        ]
        return custom_urls + urls

    def grafico_view(self, request):
        context = self.get_grafico_context()
        return render(request, 'grafico_agendamentos.html', context)

    def get_grafico_context(self):
        agendamentos_por_estabelecimento = (
            Agendamento.objects
            .values('estabelecimento__nome_estabelecimento')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
        nome_estabelecimento = [agendamento['estabelecimento__nome_estabelecimento'] for agendamento in agendamentos_por_estabelecimento]
        count_agendamentos = [agendamento['total'] for agendamento in agendamentos_por_estabelecimento]
        print(nome_estabelecimento)
        print(count_agendamentos)
        return {'nome_estabelecimento': nome_estabelecimento, 'count_agendamentos': count_agendamentos}


@admin.register(AgendamentoUsuario)
class AgendamentoUsuarioAdmin(admin.ModelAdmin):
    list_filter = ('agendamento__estabelecimento', 'usuario', 'is_active',)
    list_display = ('agendamento', 'usuario', 'get_hora_agendamento', 'is_active',)
    search_fields = ('agendamento__estabelecimento__nome_estabelecimento', 'usuario__username',)
    ordering = ('agendamento__estabelecimento', 'usuario',)
    list_editable = ['is_active'] 


    def get_hora_agendamento(self, obj):
        return obj.agendamento.hora_agendamento
    get_hora_agendamento.admin_order_field = 'agendamento__hora_agendamento' 
    get_hora_agendamento.short_description = 'Hora do Agendamento'
