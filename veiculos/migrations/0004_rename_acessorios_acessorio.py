# Generated by Django 5.0.1 on 2024-01-03 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('veiculos', '0003_rename_acessorios_veiculo_veiculo_acessorios_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Acessorios',
            new_name='Acessorio',
        ),
    ]
