from django import forms
from django.contrib.auth.forms import UserCreationForm  # Importando corretamente
from .models import Usuarios, Escola, Turma

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ['imagem_capa', 'imagem_perfil', "usu_home", "usu_email", "usu_tipo", "password1", "password2"]

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
        fields = ['tur_home_aluno', 'tur_matricula', 'tur_presenca']
        labels = {
            'tur_home_aluno': 'Nome do Aluno',
            'tur_matricula': 'Matrícula',
            'tur_presenca': 'Presença',
        }
