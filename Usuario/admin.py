from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'cpf', 'data_nascimento', 'is_active', 'is_staff']
    search_fields = ['nome_completo', 'cpf']
    list_filter = ['is_active', 'is_staff', 'data_nascimento']  # Filtros adicionais
    ordering = ['nome_completo']  # Ordenação padrão
    list_editable = ['is_active', 'is_staff']  # Permitir edição de campos diretamente na lista
    readonly_fields = ['data_nascimento', 'cpf']  # Campos somente leitura
    fieldsets = (
        (None, {'fields': ('cpf', 'nome_completo', 'data_nascimento')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        # Inclua outras seções conforme necessário
    )
    # Permitir a adição de grupos de atendimento diretamente no admin
    filter_horizontal = ('grupos_atendimento',)

    # Permite que o admin mude a senha dos usuários
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(CustomUserAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

admin.site.register(CustomUser, CustomUserAdmin)
