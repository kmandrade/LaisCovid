# Generated by Django 4.2.6 on 2023-12-31 00:48

from django.db import migrations, models
import django.db.models.deletion
import localflavor.br.models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='teve_covid_ultimos_30_dias',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='cpf',
            field=localflavor.br.models.BRCPFField(help_text='Esse campo é obrigatório. Máximo de 11 dígitos.', max_length=14, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='nome_completo',
            field=models.CharField(error_messages={'unique': 'Um usuário com este nome completo já existe.'}, max_length=150, unique=True, verbose_name='nome completo'),
        ),
        migrations.CreateModel(
            name='GrupoAtendimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('visivel', models.BooleanField(default=True)),
                ('fase', models.CharField(blank=True, max_length=10)),
                ('codigo_si_pni', models.CharField(blank=True, max_length=50)),
                ('criado_em', models.DateTimeField()),
                ('atualizado_em', models.DateTimeField()),
                ('grupo_pai', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Usuario.grupoatendimento')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='grupos_atendimento',
            field=models.ManyToManyField(blank=True, to='Usuario.grupoatendimento'),
        ),
    ]