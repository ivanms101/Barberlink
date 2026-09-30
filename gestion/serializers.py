from rest_framework import serializers
from .models import Auditoria, HorarioDia, HorarioFranja

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

class HorarioDiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioDia
        fields = [
            "hord_id",
            "hord_dia",
            "hord_activo"
        ]

class HorarioFranjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioFranja
        fields = [
            "horf_id",
            "hord",
            "horf_hora_inicio",
            "horf_hora_fin",
            "horf_activo"
        ]

    def validate(self, attrs):
        hora_inicio = attrs.get("horf_hora_inicio", getattr(self.instance, "horf_hora_inicio", None))
        hora_fin = attrs.get("horf_hora_fin", getattr(self.instance, "horf_hora_fin", None))
        dia = attrs.get("hord", getattr(self.instance, "hord", None))

        if hora_inicio >= hora_fin:
            raise serializers.ValidationError("la hora de inicio debe ser menor que la hora de fin")
        franjas = HorarioFranja.objects.filter(hord=dia, horf_activo=True)
        if self.instance:
            franjas = franjas.exclude(horf_id=self.instance.horf_id)
        for franja in franjas:
            if (hora_inicio < franja.horf_hora_fin and hora_fin > franja.horf_hora_inicio):
                raise serializers.ValidationError("La franja horaria se superpone con otra franja del mismo dia")
        return attrs