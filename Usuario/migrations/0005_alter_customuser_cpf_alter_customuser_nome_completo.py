# Generated by Django 4.2.6 on 2023-12-31 16:06

from django.db import migrations, models
import localflavor.br.models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0004_alter_customuser_is_apto_agendamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cpf',
            field=localflavor.br.models.BRCPFField(help_text='Esse campo é obrigatório. Máximo de 11 dígitos.', max_length=14, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='nome_completo',
            field=models.CharField(error_messages={'unique': 'Um usuário com este nome completo já existe.'}, max_length=150, verbose_name='nome completo'),
        ),
    ]
