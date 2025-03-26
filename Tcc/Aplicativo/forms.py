from django import forms
from django.contrib.auth.forms import UserCreationForm  # Importando corretamente
from .models import Usuarios, Escola

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
