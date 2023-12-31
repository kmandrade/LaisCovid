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


    def grupos_atendimento_display(self, obj):
        return ", ".join(obj.get_nomes_grupos_atendimento())
    grupos_atendimento_display.short_description = 'Grupos de Atendimento'

    # Permitir que o admin mude a senha dos usuários
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(CustomUserAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('grafico_usuarios/', self.admin_site.admin_view(self.grafico_usuarios_view), name='grafico-usuarios'),
        ]
        return custom_urls + urls

    def grafico_usuarios_view(self, request):
        context = self.get_user_aptitude_count()
        return render(request, 'grafico_pizza_usuario.html', context)

    def get_user_aptitude_count(self):
        aptos = CustomUser.objects.filter(is_apto_agendamento=True).count()
        inaptos = CustomUser.objects.filter(is_apto_agendamento=False).count()
        return {'aptos': aptos, 'inaptos': inaptos}
admin.site.register(CustomUser, CustomUserAdmin)
