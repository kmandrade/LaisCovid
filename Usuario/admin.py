from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'nome_completo', 'cpf', 'data_nascimento', 'is_active', 'is_staff',
        'is_superuser', 'is_apto_agendamento', 'teve_covid_ultimos_30_dias',
        'date_joined', 'grupos_atendimento_display'
    ]
    search_fields = ['nome_completo', 'cpf']
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'is_apto_agendamento',
        'teve_covid_ultimos_30_dias', 'data_nascimento'  # Adicione filtros conforme necessário
    ]
    ordering = ['nome_completo']  # Ordenação padrão
    list_editable = [
        'is_active', 'is_staff', 'is_superuser', 'is_apto_agendamento'
        # Edite conforme necessário, mas cuidado ao permitir a edição de campos importantes diretamente
    ]
    readonly_fields = ['data_nascimento', 'cpf', 'date_joined']  # Campos somente leitura
    fieldsets = (
        (None, {'fields': ('cpf', 'nome_completo', 'data_nascimento')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_apto_agendamento')}),
        ('Informações Adicionais', {'fields': ('teve_covid_ultimos_30_dias', 'date_joined', 'grupos_atendimento')}),
        # Inclua outras seções conforme necessário
    )
    # Permitir a adição de grupos de atendimento diretamente no admin
    filter_horizontal = ('grupos_atendimento',)


    def grupos_atendimento_display(self, obj):
        return ", ".join(obj.get_nomes_grupos_atendimento())
    grupos_atendimento_display.short_description = 'Grupos de Atendimento'

    # Permite que o admin mude a senha dos usuários
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(CustomUserAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
    
admin.site.register(CustomUser, CustomUserAdmin)
