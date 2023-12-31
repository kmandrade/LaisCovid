from django.db import models
from Usuario.models import CustomUser
from datetime import datetime
from django.utils.timezone import localtime
from datetime import date

class Estabelecimento(models.Model):
    nome_estabelecimento = models.CharField('Nome do Estabelecimento', max_length=70)
    codigo_cnes = models.CharField('Código CNES', max_length=30)

    def __str__(self):
        return f"{self.nome_estabelecimento}, CNES: {self.codigo_cnes}"


class Agendamento(models.Model):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, verbose_name="Estabelecimento")
    data_agendamento = models.DateField('Data do Agendamento')

    def __str__(self):
        return f"Dia {self.data_agendamento}, Estabelecimento: {self.estabelecimento}"

class AgendamentoCustomUser(models.Model):
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, verbose_name="Agendamento")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="CPF")
    is_active = models.BooleanField(default=False, verbose_name='Agendamento Ativo')
    hora_agendamento = models.TimeField('Hora do Agendamento')

    def __str__(self):
        return f"Agendamento {self.agendamento}, Candidato:{self.user}, Ativo:{self.is_active}, Hora:{self.hora_agendamento} "

    def status_agendamento(self):
        now = datetime.now()
        agendamento_datetime = datetime.combine(self.agendamento.data_agendamento, self.hora_agendamento)
        if now > agendamento_datetime:
            return 'Expirado'
        else:
            return 'Ativo'

    def datahora_consulta(self):
        return f"Sistema acessado às {localtime().time().strftime('%H:%M:%S')} no dia {date.today().strftime('%d/%m/%Y')}"

    def dia_semana(self):

        dias_semana = {
                       0: 'Quarta-Feira',
                       1: 'Quinta-Feira',
                       2: 'Sexta-Feira',
                       3: 'Sábado',
                       4: 'Domingo'}

        dia_agendamento = dias_semana[self.agendamento.data_agendamento.weekday()]
        return dia_agendamento