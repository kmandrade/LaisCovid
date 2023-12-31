from django.db import models
from datetime import date
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.timezone import localtime
from localflavor.br.models import BRCPFField
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rolepermissions.roles import assign_role


class GrupoAtendimento(models.Model):
    nome = models.CharField(max_length=100)
    visivel = models.BooleanField(default=True)
    fase = models.CharField(max_length=10, blank=True)
    codigo_si_pni = models.CharField(max_length=50, blank=True)
    grupo_pai = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField()
    atualizado_em = models.DateTimeField()

    def __str__(self):
        return self.nome
   
class CustomUserManager(BaseUserManager):

    def create_user(self, nome_completo, data_nascimento, cpf, password=None, teve_covid_ultimos_30_dias=False, nomes_grupos_atendimento=[], **extra_fields):
        
        if not cpf:
            raise ValueError('O campo CPF é obrigatório.')

        user = self.model(
            nome_completo=nome_completo,
            data_nascimento=data_nascimento,
            cpf=cpf,
            teve_covid_ultimos_30_dias=teve_covid_ultimos_30_dias,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        # Associar os grupos de atendimento pelo nome
        for nome_grupo in nomes_grupos_atendimento:
            try:
                grupo = GrupoAtendimento.objects.get(nome=nome_grupo)
                user.grupos_atendimento.add(grupo)
            except GrupoAtendimento.DoesNotExist:
                print(f"Grupo de atendimento não encontrado: {nome_grupo}")

        return user
    
    def create_superuser(self, cpf, nome_completo, data_nascimento, password = None):

        user = self.create_user(
            nome_completo = nome_completo,
            data_nascimento=data_nascimento,
            cpf=cpf,
            password= password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
    
class CustomUser(AbstractBaseUser, PermissionsMixin):

    cpf = BRCPFField(
        max_length=11,
        unique=False,
        verbose_name='CPF',
        help_text='Esse campo é obrigatório. Máximo de 11 dígitos.',
    )

    nome_completo = models.CharField(
        'nome completo',
        max_length=150,
        blank=False,
        unique=True,
        error_messages={
            'unique': "Um usuário com este nome completo já existe.",
        },
    )
    data_nascimento = models.DateField(('data de nascimento'))
    is_apto_agendamento = models.BooleanField(default=True, verbose_name='Ativo')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    is_staff = models.BooleanField(default=False, verbose_name='Faz parte da Administração')
    is_admin = models.BooleanField(default =False, verbose_name=('Administrador'))
    is_superuser = models.BooleanField(default=False, verbose_name=('Superuser'))
    date_joined = models.DateTimeField(auto_now_add=True,verbose_name=('Data de Ingresso'))
    grupos_atendimento = models.ManyToManyField(GrupoAtendimento, blank=True)
    teve_covid_ultimos_30_dias = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'nome_completo'
    REQUIRED_FIELDS = ['cpf', 'data_nascimento']

    def get_idade(self):
            data_nascimento = self.data_nascimento
            idade = relativedelta(date.today(), data_nascimento).years
            return idade


