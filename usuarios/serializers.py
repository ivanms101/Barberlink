from rest_framework import serializers
from .models import Usuario, Rol

class UsuarioSerializer(serializers.ModelSerializer):
    usua_activo = serializers.BooleanField(read_only=True)
    usua_rol_desc = serializers.CharField(source="usua_rol.rol_desc", read_only=True)
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
            "usua_rol_desc",
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

class UsuarioRegistroSerializer(serializers.ModelSerializer):
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
        ]
    def create(self, validated_data):
        password = validated_data.pop("password")
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.usua_rol = Rol.objects.get(rol_nomb="usua")
        usuario.save()
        return usuario

class UsuarioPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

class UsuarioEstadoSerializer(serializers.Serializer):
    usua_activo = serializers.BooleanField()

class UsuarioPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            "usua_id",
            "usua_nomb",
            "usua_tp_doc",
            "usua_doc_id",
            "usua_tel",
            "usua_cor"
        ]
        read_only_fields = [
            "usua_id",
            "usua_tp_doc",
            "usua_doc_id"
        ]

class UsuarioCambioPasswordSerializer(serializers.Serializer):
    password_actual = serializers.CharField(write_only=True)
    password_nueva = serializers.CharField(write_only=True)
    def validate(self, attrs):
        usuario = self.context["usuario"]
        if not usuario.check_password(attrs["password_actual"]):
            raise serializers.ValidationError({
                "password_actual": "La contraseña actual es incorrecta"
            })
        return attrs