from rest_framework import serializers
from .models import Auditoria

class AuditoriaSerializer(serializers.ModelSerializer):
    nombre_usuario = serializers.SerializerMethodField()
    def get_nombre_usuario(self, obj):
        return obj.usuario.usua_nomb
    class Meta:
        model = Auditoria
        fields = [
            "id",
            "nombre_usuario",
            "accion",
            "tabla",
            "registro",
            "fecha",
            "observacion"
        ]