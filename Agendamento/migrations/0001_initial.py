# Generated by Django 4.2.6 on 2023-12-31 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_agendamento', models.DateField(verbose_name='Data do Agendamento')),
            ],
        ),
        migrations.CreateModel(
            name='Estabelecimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_estabelecimento', models.CharField(max_length=70, verbose_name='Nome do Estabelecimento')),
                ('codigo_cnes', models.CharField(max_length=30, verbose_name='Código CNES')),
            ],
        ),
        migrations.CreateModel(
            name='AgendamentoCustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Agendamento Ativo')),
                ('hora_agendamento', models.TimeField(verbose_name='Hora do Agendamento')),
                ('agendamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agendamento.agendamento', verbose_name='Agendamento')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='CPF')),
            ],
        ),
        migrations.AddField(
            model_name='agendamento',
            name='estabelecimento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agendamento.estabelecimento', verbose_name='Estabelecimento'),
        ),
    ]
