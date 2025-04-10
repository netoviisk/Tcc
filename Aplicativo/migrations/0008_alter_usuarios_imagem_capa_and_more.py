# Generated by Django 5.1.6 on 2025-03-27 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicativo', '0007_usuarios_imagem_capa_usuarios_imagem_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='imagem_capa',
            field=models.ImageField(blank=True, default='capa/fundo.jpg', null=True, upload_to='capa/'),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='imagem_perfil',
            field=models.ImageField(blank=True, default='perfil/profile_icon.jpg', null=True, upload_to='perfil/'),
        ),
    ]
