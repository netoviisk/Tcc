from django.contrib.auth.backends import ModelBackend
from models import Usuarios

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            usuario = Usuarios.objects.get(usu_email=username)
            if usuario.check_password(password):  # Verifica a senha corretamente
                return usuario
        except Usuarios.DoesNotExist:
            return None
