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
        ]