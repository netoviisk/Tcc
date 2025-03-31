from django import forms
from .models import Usuarios, Tarefas

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['usu_nome', 'usu_email']
        labels = {
            'usu_nome': 'Nome de Usuário',
            'usu_email': 'E-mail',
        }
        widgets = {
            'usu_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do usuário'}),
            'usu_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email do usuário'}),
        }

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefas
        fields = ['tar_descricao', 'tar_setor', 'tar_prioridade', 'tar_status', 'tar_data', 'usu_codigo']  # Campos para o formulário
        labels = {
            'tar_descricao': 'Descrição da Tarefa',
            'tar_setor': 'Setor',
            'tar_prioridade': 'Prioridade',
            'tar_status': 'Status',
            'tar_data': 'Data da Tarefa',
            'usu_codigo': 'Usuário Responsável',
        }
        widgets = {
            'tar_descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição da tarefa'}),
            'tar_setor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Setor da tarefa'}),
            'tar_prioridade': forms.Select(attrs={'class': 'form-control'}),
            'tar_status': forms.Select(attrs={'class': 'form-control'}),
            'tar_data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'usu_codigo': forms.Select(attrs={'class': 'form-control'}),
        }
