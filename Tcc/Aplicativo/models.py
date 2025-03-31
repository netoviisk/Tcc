from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
import random
import string

# Gerador de código único
def generate_unique_code():
    while True:
        code = ''.join(random.choices(string.digits, k=8))
        if not Usuarios.objects.filter(codigo_unico=code).exists():
            return code

# Manager para Usuários
class UsuarioManager(BaseUserManager):
    def create_user(self, usu_email, password=None, **extra_fields):
        if not usu_email:
            raise ValueError("O e-mail é obrigatório")

        # Criação do usuário com e-mail
        user = self.model(usu_email=self.normalize_email(usu_email), **extra_fields)
        user.set_password(password)  # Salva a senha de forma segura
        user.save(using=self._db)
        return user

    def create_superuser(self, usu_email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(usu_email, password, **extra_fields)

# Modelo de Usuario
class Usuarios(AbstractBaseUser, PermissionsMixin):
    codigo_unico = models.CharField(max_length=8)
    usu_email = models.EmailField(unique=True, verbose_name="E-mail")
    usu_home = models.CharField(max_length=150, verbose_name="Nome de Usuário")
    usu_tipo = models.CharField(max_length=50, choices=[("professor", "Professor"), ("administrador", "Administrador")])
    escolas = models.ManyToManyField('Escola', blank=True, related_name="usuarios_associados_usuario")  # Relacionamento com Escola
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name="usuarios_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="usuarios_permissions", blank=True)

    imagem_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True, default='perfil/profile_icon.jpg')
    imagem_capa = models.ImageField(upload_to='capa/', blank=True, null=True, default='capa/fundo.jpg')

    objects = UsuarioManager()

    USERNAME_FIELD = "usu_email"
    REQUIRED_FIELDS = ["usu_home"]

    def __str__(self):
        return self.usu_email

    # Método que associa o usuário a uma escola
    def associar_escola(self, escola):
        if self.usu_tipo == "administrador" and not self.escolas.exists():
            self.escolas.add(escola)
            self.save()


# Modelo Escola
class Escola(models.Model):
    esc_desc = models.TextField()
    esc_name = models.CharField(max_length=100)
    sala = models.CharField(max_length=100)

    # Relacionamento ManyToMany com o modelo Usuarios
    usuarios_associados = models.ManyToManyField(Usuarios, related_name='escolas_associadas_escola')  # Ajustado para usar 'Usuarios'

    def __str__(self):
        return self.esc_name

# Modelo Professor
class Professor(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='professores')  # Ajustado para usar 'Usuarios'

    def __str__(self):
        return f"Professor: {self.usuario.usu_home}"

# Modelo Sala
class Sala(models.Model):
    sal_name = models.CharField(max_length=45)
    sal_desc = models.CharField(max_length=45)
    sal_cod_acesso = models.CharField(max_length=6)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='salas')

    def __str__(self):
        return self.sal_name

# Modelo Turma
class Turma(models.Model):
    tur_home_aluno = models.CharField(max_length=45)
    tur_matricula = models.CharField(max_length=100)
    tur_presenca = models.CharField(max_length=45)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='turmas')

    def __str__(self):
        return f"Turma {self.tur_home_aluno}"

# Modelo Evento
class Evento(models.Model):
    eve_nome = models.CharField(max_length=45)
    eve_descricao = models.CharField(max_length=1000)
    eve_data = models.DateTimeField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, null=True, blank=True, related_name='eventos')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, null=True, blank=True, related_name='eventos')

    def __str__(self):
        return self.eve_nome
