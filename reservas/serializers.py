from rest_framework import serializers
from .models import Reserva, DetalleReserva
from usuarios.models import Usuario
from servicios.models import Servicio

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = [
            "id",
            "cliente",
            "barbero",
            "fecha",
            "hora",
            "estado"
        ]

class DetalleReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleReserva
        fields = [
            "id",
            "reserva",
            "servicio"
        ]

class ProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            "usua_id",
            "usua_nomb"
        ]

class ServicioDisponibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = [
            "serv_id",
            "serv_nomb",
            "serv_tari",
        ]

class ReservaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = [
            "barbero",
            "fecha",
            "hora",
        ]