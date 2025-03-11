from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now

class UsuarioManager(BaseUserManager):
    def create_user(self, usu_email, usu_home, usu_senha, usu_tipo):
        if not usu_email:
            raise ValueError("O email deve ser informado")
        usuario = self.model(
            usu_email=self.normalize_email(usu_email),
            usu_home=usu_home,
            usu_tipo=usu_tipo
        )
        usuario.set_password(usu_senha)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, usu_email, usu_home, usu_senha):
        usuario = self.create_user(
            usu_email=usu_email,
            usu_home=usu_home,
            usu_senha=usu_senha,
            usu_tipo="administrador"
        )
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario

class Usuarios(AbstractBaseUser, PermissionsMixin):
    TIPO_USUARIO_CHOICES = [
        ('professor', 'Professor'),
        ('administrador', 'Administrador')
    ]

    usu_home = models.CharField(max_length=100, verbose_name="Nome de Usuário")
    usu_email = models.EmailField(max_length=100, unique=True, verbose_name="Email")
    usu_tipo = models.CharField(
        max_length=15,
        verbose_name="Cadastrar Como",
        choices=TIPO_USUARIO_CHOICES
    )
    last_login = models.DateTimeField(default=now)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="usuarios_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="usuarios_permissions_set",
        blank=True
    )

    objects = UsuarioManager()

    USERNAME_FIELD = 'usu_email'
    REQUIRED_FIELDS = ['usu_home', 'usu_tipo']

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
        return f"Professor {self.usuario.usu_email}"

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
