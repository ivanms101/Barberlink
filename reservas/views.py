from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response  import Response

from .models import Reserva, DetalleReserva
from .serializers import ReservaSerializer, DetalleReservaSerializer, ProfesionalSerializer, ServicioDisponibleSerializer

from usuarios.models import Usuario
from servicios.models import Servicio

@login_required
def reservas(request):
    return render(request, "reservas/reservas.html")

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]

@api_view(["GET"])
def profesionales(request):
    profesionales = Usuario.objects.filter(
        usua_activo = True,
        usua_rol__rol_nomb = "empl"
    )
    serializer = ProfesionalSerializer(profesionales, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def servicios_disponibles(request):
    servicios = Servicio.objects.filter(
        serv_activo = True
    )
    serializer = ServicioDisponibleSerializer(servicios, many=True)
    return Response(serializer.data)
