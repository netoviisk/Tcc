from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, usu_email, password=None, **extra_fields):
        if not usu_email:
            raise ValueError("O e-mail é obrigatório")

        user = self.model(usu_email=self.normalize_email(usu_email), **extra_fields)
        user.set_password(password)  # Salva a senha de forma segura
        user.save(using=self._db)
        return user

    def create_superuser(self, usu_email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(usu_email, password, **extra_fields)

class Usuarios(AbstractBaseUser, PermissionsMixin):
    usu_email = models.EmailField(unique=True, verbose_name="E-mail")
    usu_home = models.CharField(max_length=150, verbose_name="Nome de Usuário")
    usu_tipo = models.CharField(max_length=50, choices=[("professor", "Professor"), ("administrador", "Administrador")])

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="usuarios_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="usuarios_permissions", blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = "usu_email"
    REQUIRED_FIELDS = ["usu_home"]

    def __str__(self):
        return self.usu_email

class Escola(models.Model):
    esc_name = models.CharField(max_length=45)
    esc_desc = models.CharField(max_length=1000)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return self.esc_name

class Professor(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return f"Professor: {self.usuario.usu_home}"

class Sala(models.Model):
    sal_name = models.CharField(max_length=45)
    sal_desc = models.CharField(max_length=45)
    sal_cod_acesso = models.CharField(max_length=6)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)

    def __str__(self):
        return self.sal_name

class Turma(models.Model):
    tur_home_aluno = models.CharField(max_length=45)
    tur_presenca = models.CharField(max_length=45)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Turma {self.tur_home_aluno}"

class Evento(models.Model):
    eve_nome = models.CharField(max_length=45)
    eve_descricao = models.CharField(max_length=1000)
    eve_data = models.DateTimeField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, null=True, blank=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.eve_nome
