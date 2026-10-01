from rest_framework import serializers
from .models import Pago

class PagoSerializer(serializers.ModelSerializer):
    nombre_cliente = serializers.SerializerMethodField()
    nombre_servicio = serializers.SerializerMethodField()
    fecha = serializers.SerializerMethodField()
    hora = serializers.SerializerMethodField()
    nombre_barbero = serializers.SerializerMethodField()
    valor = serializers.SerializerMethodField()
    def get_nombre_cliente(self, obj):
        return obj.reserva.cliente.usua_nomb
    def get_nombre_servicio(self, obj):
        return obj.reserva.detalles.all()[0].servicio.serv_nomb
    def get_fecha(self, obj):
        return obj.reserva.fecha
    def get_hora(self, obj):
        return obj.reserva.hora
    def get_nombre_barbero(self, obj):
        return obj.reserva.barbero.usua_nomb
    def get_valor(self, obj):
        return obj.reserva.detalles.all()[0].servicio.serv_tari
    class Meta:
        model = Pago
        fields = [
            "id",
            "reserva",
            "valor",
            "metodo",
            "estado",
            "nombre_cliente",
            "nombre_servicio",
            "fecha",
            "hora",
            "nombre_barbero",
        ]

class PagoActualizarSerializer(serializers.ModelSerializer):
    valor = serializers.SerializerMethodField()
    def get_valor(self,obj):
        return obj.reserva.detalles.all()[0].servicio.serv_tari
    class Meta:
        model = Pago
        fields = [
            "valor",
            "metodo",
            "estado"
        ]