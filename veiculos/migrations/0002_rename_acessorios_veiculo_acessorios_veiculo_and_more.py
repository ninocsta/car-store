# Generated by Django 5.0.1 on 2024-01-03 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('veiculos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='veiculo',
            old_name='acessorios',
            new_name='acessorios_veiculo',
        ),
        migrations.RenameField(
            model_name='veiculo',
            old_name='marca',
            new_name='marca_veiculo',
        ),
    ]
