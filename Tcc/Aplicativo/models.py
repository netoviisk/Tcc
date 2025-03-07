from django.db import models

class Usuarios(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('professor', 'Professor'),
        ('admin', 'Administrador')
    ]

    usu_home = models.CharField(max_length=45, verbose_name="Nome de Usuário")
    usu_email = models.CharField(max_length=45, verbose_name="Email")
    usu_senha = models.CharField(max_length=45, verbose_name="Senha")
    usu_tipo = models.CharField(
        max_length=45,
        verbose_name="Cadastrar Como",
        choices=TIPO_USUARIO_CHOICES
    )

    def __str__(self):
        return self.usu_email

    def save(self, *args, **kwargs):
        """ Salva o usuário e cria a relação correta com Professores ou Escola """
        super().save(*args, **kwargs)  # Salva o usuário primeiro

        if self.usu_tipo == "professor":
            # Criar professor associado ao usuário
            if not Professores.objects.filter(Usuarios_idUsuarios=self).exists():
                Professores.objects.create(Usuarios_idUsuarios=self)

        elif self.usu_tipo == "admin":
            # Criar escola associada ao usuário
            if not Escola.objects.filter(Usuarios_idUsuarios=self).exists():
                Escola.objects.create(
                    esc_name=f"Escola de {self.usu_home}",
                    esc_desc="Descrição Padrão",
                    Usuarios_idUsuarios=self
                )

class Escola(models.Model):
    esc_name = models.CharField(max_length=45)
    esc_desc = models.CharField(max_length=1000)
    Usuarios_idUsuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return self.esc_name

class Professores(models.Model):
    Usuarios_idUsuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return f"Professor {self.Usuarios_idUsuarios.usu_email}"

class Sala(models.Model):
    sal_name = models.CharField(max_length=45)
    sal_desc = models.CharField(max_length=45)
    sal_cod_acesso = models.CharField(max_length=6)
    Escola_idEscola = models.ForeignKey(Escola, on_delete=models.CASCADE)

    def __str__(self):
        return self.sal_name

class Turmas(models.Model):
    tur_home_aluno = models.CharField(max_length=45)
    tur_presenca = models.CharField(max_length=45)
    Professores_idProfessores = models.ForeignKey(Professores, on_delete=models.CASCADE)

    def __str__(self):
        return f"Turma {self.tur_home_aluno}"

class Eventos(models.Model):
    eve_nome = models.CharField(max_length=45)
    eve_descricao = models.CharField(max_length=1000)
    eve_data = models.DateTimeField()
    Turmas_idTurmas = models.ForeignKey(Turmas, on_delete=models.CASCADE, null=True, blank=True)
    Sala_idSala = models.ForeignKey(Sala, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.eve_nome
