from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    usua_activo = serializers.BooleanField(read_only=True)
    class Meta:
        model = Usuario
        fields = [
            "usua_id",
            "usua_nomb",
            "usua_tp_doc",
            "usua_doc_id",
            "usua_tel",
            "usua_cor",
            "usua_rol",
            "usua_activo",
        ]

class UsuarioCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = Usuario
        fields = [
            "usua_nomb",
            "usua_tp_doc",
            "usua_doc_id",
            "usua_tel",
            "usua_cor",
            "password",
            "usua_rol"
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario

class UsuarioPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

class UsuarioEstadoSerializer(serializers.Serializer):
    usua_activo = serializers.BooleanField()