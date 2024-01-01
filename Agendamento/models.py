from django.db import models
from Usuario.models import CustomUser
from datetime import datetime
from django.utils.timezone import localtime
from datetime import time

class Estabelecimento(models.Model):
    nome_estabelecimento = models.CharField('Nome do Estabelecimento', max_length=70)
    codigo_cnes = models.CharField('Código CNES', max_length=30)

    def __str__(self):
        return f"{self.nome_estabelecimento}, CNES: {self.codigo_cnes}"


class Agendamento(models.Model):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, verbose_name="Estabelecimento")
    data_agendamento = models.DateField('Data do Agendamento')
    hora_agendamento = models.TimeField('Hora do Agendamento', default=time(13, 0))
    vagas_disponiveis = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.data_agendamento} às {self.hora_agendamento} - {self.estabelecimento}"

    class Meta:
        unique_together = ('estabelecimento', 'data_agendamento', 'hora_agendamento')


class AgendamentoUsuario(models.Model):
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, verbose_name="Agendamento")
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Usuário")
    is_active = models.BooleanField(default=False, verbose_name='Agendamento Ativo')

    def __str__(self):
        return f"Agendamento: {self.agendamento}, Usuário: {self.usuario}, Ativo: {self.is_active}"

    def status_agendamento(self):
        agora = datetime.now()
        data_hora_agendamento = datetime.combine(self.agendamento.data_agendamento, self.agendamento.hora_agendamento)
        return 'Expirado' if agora > data_hora_agendamento else 'Ativo'

    def dia_semana(self):
        dias_semana = {0: 'Quarta-Feira', 1: 'Quinta-Feira', 2: 'Sexta-Feira', 3: 'Sábado', 4: 'Domingo'}
        return dias_semana[self.agendamento.data_agendamento.weekday()]

    class Meta:
        unique_together = ('usuario', 'is_active')
