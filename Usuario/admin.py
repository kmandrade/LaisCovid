from django.contrib import admin
from .models import CustomUser
from django.urls import path
from django.shortcuts import render

class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'nome_completo', 'cpf', 'data_nascimento', 'is_active', 'is_staff',
        'is_superuser', 'is_apto_agendamento', 'teve_covid_ultimos_30_dias',
        'date_joined', 'grupos_atendimento_display'
    ]
    search_fields = ['nome_completo', 'cpf']
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'is_apto_agendamento',
        'teve_covid_ultimos_30_dias', 'data_nascimento'
    ]
    ordering = ['nome_completo']  
    list_editable = [ #Edicao de campos da entidade
        'is_active', 'is_staff', 'is_superuser', 'is_apto_agendamento'
    ]
    readonly_fields = ['data_nascimento', 'cpf', 'date_joined']  # Campos somente leitura
    fieldsets = (
        (None, {'fields': ('cpf', 'nome_completo', 'data_nascimento')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_apto_agendamento')}),
        ('Informações Adicionais', {'fields': ('teve_covid_ultimos_30_dias', 'date_joined', 'grupos_atendimento')}),
    )
    # Permitir a adição de grupos de atendimento diretamente no admin
    filter_horizontal = ('grupos_atendimento',)
    actions = ['delete_selected']

    #Exibindo de forma personalizada os grupos de atendimentos associadas ao usuario.
    def grupos_atendimento_display(self, obj):
        return ", ".join(obj.get_nomes_grupos_atendimento())
    grupos_atendimento_display.short_description = 'Grupos de Atendimento'

    #Personalizando a url padrao do django admin
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('grafico_usuarios/', self.admin_site.admin_view(self.grafico_usuarios_view), name='grafico-usuarios'),
        ]
        return custom_urls + urls

    #Rendereiza o html com o contexto populado
    def grafico_usuarios_view(self, request):
        context = self.get_user_aptitude_count()
        return render(request, 'grafico_pizza_usuario.html', context)

    #Contador de usuarios aptos e inaptos
    def get_user_aptitude_count(self):
        aptos = CustomUser.objects.filter(is_apto_agendamento=True).count()
        inaptos = CustomUser.objects.filter(is_apto_agendamento=False).count()
        return {'aptos': aptos, 'inaptos': inaptos}
admin.site.register(CustomUser, CustomUserAdmin)
