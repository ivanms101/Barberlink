from rest_framework import serializers
from .models import Reserva, DetalleReserva
from usuarios.models import Usuario
from servicios.models import Servicio

class UsuarioReservaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = [
            "usua_id",
            "usua_nomb"
        ]

class ServicioReservaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Servicio
        fields = [
            "serv_id",
            "serv_nomb",
            "serv_tari",
            "serv_duracion"
        ]

class ReservaSerializer(serializers.ModelSerializer):

    cliente = UsuarioReservaSerializer(read_only=True)
    barbero = UsuarioReservaSerializer(read_only=True)
    servicio = serializers.SerializerMethodField()

    class Meta:
        model = Reserva
        fields = [
            "id",
            "cliente",
            "barbero",
            "servicio",
            "fecha",
            "hora",
            "estado"
        ]

    def get_servicio(self, obj):
        detalle = obj.detalles.select_related("servicio").first()

        if detalle is None:
            return None

        return ServicioReservaSerializer(detalle.servicio).data

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
            "serv_duracion"
        ]

class ReservaCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserva
        fields = [
            "cliente",
            "barbero",
            "fecha",
            "hora",
        ]
        extra_kwargs = {
            "cliente": {
                "required": False
            }
        }