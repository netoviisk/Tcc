from django.db import models

class Usuarios(models.Model):
    usu_codigo = models.AutoField(primary_key=True)
    usu_nome = models.CharField(max_length=45, verbose_name='Nome de Usuário')
    usu_email = models.EmailField(max_length=45, unique=True, verbose_name='E-mail')

    def __str__(self):
        return self.usu_nome

    class Meta:
        db_table = 'usuarios'


class Tarefas(models.Model):
    tar_codigo = models.AutoField(primary_key=True)
    tar_descricao = models.CharField(max_length=45, verbose_name='Descrição da Tarefa')
    tar_setor = models.CharField(max_length=45, verbose_name='Setor')

    PRIORIDADE_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Média'),
        ('baixa', 'Baixa'),
    ]
    tar_prioridade = models.CharField(
        max_length=6, choices=PRIORIDADE_CHOICES, default='media', verbose_name='Prioridade'
    )

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_progresso', 'Em Progresso'),
        ('concluida', 'Concluída'),
    ]
    tar_status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='pendente', verbose_name='Status'
    )

    tar_data = models.DateField(verbose_name='Data')  # Data da tarefa
    usu_codigo = models.ForeignKey(
        'Usuarios', on_delete=models.CASCADE, to_field='usu_codigo', verbose_name='Usuário'
    )

    def __str__(self):
        return self.tar_descricao

    class Meta:
        db_table = 'tarefas'
