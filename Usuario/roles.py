from datetime import date
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.timezone import localtime
from localflavor.br.models import BRCPFField
from datetime import datetime
from dateutil.relativedelta import relativedelta



class CustomUserManager(BaseUserManager):

    def create_user(self, nome_completo,data_nascimento, cpf, fl_apto_agendamento ,password = None):

        if not cpf:
            raise ValueError(('O campo CPF é obrigatório.'))

        user = self.model(
            nome_completo = nome_completo,
            data_nascimento = data_nascimento,
            cpf = cpf,
            fl_apto_agendamento = fl_apto_agendamento
        )

        user.set_password(password)
        user.save(using = self._db)
        return user
    
class CustomUser(AbstractBaseUser, PermissionsMixin):

    cpf = BRCPFField(
        max_length = 11,
        unique = True,
        verbose_name = ('CPF'),
        help_text = ('Esse campo é obrigatório. Máximo de 11 dígitos.'),
        error_messages = {
            'unique': ("Esse CPF já é cadastrado no sistema."),
        },
    )

    nome_completo = models.CharField(('nome completo'), max_length=150, blank=False)
    data_nascimento = models.DateField(('data de nascimento'))
    is_apto_agendamento = models.BooleanField(default=True, verbose_name='Ativo')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    is_staff = models.BooleanField(default=False, verbose_name='Faz parte da Administração')
    is_admin = models.BooleanField(default =False, verbose_name=('Administrador'))
    is_superuser = models.BooleanField(default=False, verbose_name=('Superuser'))
    date_joined = models.DateTimeField(auto_now_add=True,verbose_name=('Data de Ingresso'))


    objects = CustomUserManager()

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome_completo','data_nascimento']

def get_idade(self):
        data_nascimento = self.data_nascimento
        idade = relativedelta(date.today(), data_nascimento).years
        return idade