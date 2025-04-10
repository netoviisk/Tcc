from django import forms
from django.contrib.auth.forms import UserCreationForm  # Importando corretamente
from .models import Usuarios, Escola, Turma, Sala

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ["usu_home", "usu_email", "usu_tipo", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["usu_home"].widget.attrs.update({"placeholder": "Nome de Usuário"})
        self.fields["usu_email"].widget.attrs.update({"placeholder": "Email"})

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = ['esc_name', 'esc_desc']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['usu_home', 'usu_email', 'imagem_perfil', 'imagem_capa']
        widgets = {
            'usu_home': forms.TextInput(attrs={'class': 'form-control'}),
            'usu_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['tur_home_aluno', 'tur_matricula', 'sala']
        labels = {
            'tur_home_aluno': 'Nome do Aluno',
            'tur_matricula': 'Matrícula',
            'sala': 'Sala',
        }
        widgets = {
            'tur_home_aluno': forms.TextInput(attrs={'placeholder': 'Digite o nome do Aluno'}),
            'tur_matricula': forms.TextInput(attrs={'placeholder': 'Digite o número de Matrícula'}),
            'sala': forms.Select(attrs={'placeholder': 'Selecione uma sala'}),
        }


class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['sal_name', 'sal_desc', 'sal_cod_acesso']
        labels = {
            'sal_name': 'Nome da Sala',
            'sal_desc': 'Descrição',
            'sal_cod_acesso': 'Código de Acesso',
        }
        widgets = {
            'sal_name': forms.TextInput(attrs={'placeholder': 'Digite o nome da sala'}),
            'sal_desc': forms.TextInput(attrs={'placeholder': 'Digite uma descrição'}),
            'sal_cod_acesso': forms.TextInput(attrs={'placeholder': 'Ex: ABC123'}),
        }
