from django.db import models

class Usuarios(models.Model):
    usu_home = models.CharField(max_length=45)
    usu_email = models.CharField(max_length=45)
    usu_senha = models.CharField(max_length=45)
    usu_tipo = models.CharField(max_length=45)

    def _str_(self):
        return self.usu_email

class Escola(models.Model):
    esc_name = models.CharField(max_length=45)
    esc_desc = models.CharField(max_length=1000)
    Usuarios_idUsuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def _str_(self):
        return self.esc_name

class Professores(models.Model):
    Usuarios_idUsuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def _str_(self):
        return f"Professor {self.Usuarios_idUsuarios.usu_email}"

class Sala(models.Model):
    sal_name = models.CharField(max_length=45)
    sal_desc = models.CharField(max_length=45)
    sal_cod_acesso = models.CharField(max_length=6)
    Escola_idEscola = models.ForeignKey(Escola, on_delete=models.CASCADE)

    def _str_(self):
        return self.sal_name

class Turmas(models.Model):
    tur_home_aluno = models.CharField(max_length=45)
    tur_presenca = models.CharField(max_length=45)
    Professores_idProfessores = models.ForeignKey(Professores, on_delete=models.CASCADE)

    def _str_(self):
        return f"Turma {self.tur_home_aluno}"

class Eventos(models.Model):
    eve_nome = models.CharField(max_length=45)
    eve_descricao = models.CharField(max_length=1000)
    eve_data = models.DateTimeField()
    Turmas_idTurmas = models.ForeignKey(Turmas, on_delete=models.CASCADE, null=True, blank=True)
    Sala_idSala = models.ForeignKey(Sala, on_delete=models.CASCADE, null=True, blank=True)

    def _str_(self):
        return self.eve_nome

# Create your models here.
