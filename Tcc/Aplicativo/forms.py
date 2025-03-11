from django import forms
from .models import Usuarios, Escola

class UsuarioForm(forms.ModelForm):
    TIPO_USUARIO_CHOICES = [
        ('professor', 'Professor'),
        ('administrador', 'Administrador'),
    ]

    usu_senha = forms.CharField(
        widget=forms.PasswordInput(),
        label="Senha"
    )

    usu_tipo = forms.ChoiceField(
        choices=TIPO_USUARIO_CHOICES,
        widget=forms.RadioSelect,
        label="Tipo de Usuário"
    )

    class Meta:
        model = Usuarios
        fields = ['usu_home', 'usu_email', 'usu_senha', 'usu_tipo']

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['usu_senha'])  # Garante que a senha será armazenada com hash
        if commit:
            usuario.save()
        return usuario

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = ['esc_name', 'esc_desc']
