from django import forms
from .models import Usuarios, Escola

class UsuarioForm(forms.ModelForm):
    TIPO_USUARIO_CHOICES = [
        ('professor', 'Professor'),
        ('usuario', 'Usuário'),
    ]

    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIO_CHOICES, widget=forms.RadioSelect)
    esc_name = forms.CharField(max_length=45, required=False, label="Nome da Escola")

    class Meta:
        model = Usuarios
        fields = ['usu_home', 'usu_email', 'usu_senha', 'tipo_usuario', 'esc_name']