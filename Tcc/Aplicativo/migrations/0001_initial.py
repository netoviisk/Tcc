# Generated by Django 5.1.6 on 2025-03-24 11:07

import Aplicativo.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Escola',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_unico', models.CharField(default=Aplicativo.models.generate_unique_code, editable=False, max_length=8, unique=True)),
                ('esc_name', models.CharField(max_length=45)),
                ('esc_desc', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sal_name', models.CharField(max_length=45)),
                ('sal_desc', models.CharField(max_length=45)),
                ('sal_cod_acesso', models.CharField(max_length=6)),
                ('escola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicativo.escola')),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tur_home_aluno', models.CharField(max_length=45)),
                ('tur_presenca', models.CharField(max_length=45)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicativo.professor')),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eve_nome', models.CharField(max_length=45)),
                ('eve_descricao', models.CharField(max_length=1000)),
                ('eve_data', models.DateTimeField()),
                ('sala', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Aplicativo.sala')),
                ('turma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Aplicativo.turma')),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('usu_email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('usu_home', models.CharField(max_length=150, verbose_name='Nome de Usuário')),
                ('usu_tipo', models.CharField(choices=[('professor', 'Professor'), ('administrador', 'Administrador')], max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='usuarios_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='usuarios_permissions', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='professor',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='escola',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
