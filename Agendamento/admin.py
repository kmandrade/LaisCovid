from django.contrib import admin
from .models import Estabelecimento

class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ('nome_estabelecimento', 'codigo_cnes')
    search_fields = ['nome_estabelecimento', 'codigo_cnes']

admin.site.register(Estabelecimento, EstabelecimentoAdmin)
