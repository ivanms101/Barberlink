from rest_framework import serializers
from .models import Servicio

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = [
            "serv_id",
            "serv_nomb",
            "serv_tari",
            "serv_activo",
            "serv_duracion",
        ]
    def validate_serv_duracion(self, value):
        if value < 15:
            raise serializers.ValidationError("La duracion debe ser de almenos 15 minutos")
        if value % 15 != 0:
            raise serializers.ValidationError("La duracion debe ser multiplo de 15 minutos")
        return value