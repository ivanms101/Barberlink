from django.contrib.auth.backends import ModelBackend
from .models import Usuario

class UsuarioBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        documento = kwargs.get("usua_doc_id")
        if documento is None:
            return None
        try:
            usuario = Usuario.objects.get(usua_doc_id = documento)
        except Usuario.DoesNotExist:
            return None
        if not usuario.usua_activo:
            return None
        if usuario.check_password(password):
            return usuario
        return None