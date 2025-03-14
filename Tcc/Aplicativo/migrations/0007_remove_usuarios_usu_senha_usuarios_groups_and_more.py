# Generated by Django 4.2.20 on 2025-03-11 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("Aplicativo", "0006_usuarios_last_login_alter_usuarios_usu_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usuarios",
            name="usu_senha",
        ),
        migrations.AddField(
            model_name="usuarios",
            name="groups",
            field=models.ManyToManyField(
                blank=True, related_name="usuarios_set", to="auth.group"
            ),
        ),
        migrations.AddField(
            model_name="usuarios",
            name="is_superuser",
            field=models.BooleanField(
                default=False,
                help_text="Designates that this user has all permissions without explicitly assigning them.",
                verbose_name="superuser status",
            ),
        ),
        migrations.AddField(
            model_name="usuarios",
            name="password",
            field=models.CharField(default=1, max_length=128, verbose_name="password"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="usuarios",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                related_name="usuarios_permissions_set",
                to="auth.permission",
            ),
        ),
        migrations.AlterField(
            model_name="usuarios",
            name="usu_email",
            field=models.EmailField(max_length=100, unique=True, verbose_name="Email"),
        ),
    ]
