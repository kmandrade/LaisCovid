# Generated by Django 4.2.6 on 2024-01-12 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Agendamento', '0003_alter_agendamentousuario_is_active'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='agendamentousuario',
            unique_together=set(),
        ),
    ]
