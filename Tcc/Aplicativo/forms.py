from django import forms
from .models import Usuarios, Escola

class UsuarioForm(forms.ModelForm):
    TIPO_USUARIO_CHOICES = [
        ('professor', 'Professor'),
        ('usuario', 'Usuário'),
    ]

    usu_tipo = forms.ChoiceField(choices=TIPO_USUARIO_CHOICES, widget=forms.RadioSelect)  # Correção aqui: use usu_tipo
    class Meta:
        model = Usuarios
        fields = ['usu_home', 'usu_email', 'usu_senha', 'usu_tipo'] # Removido o esc_name

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = ['esc_name']