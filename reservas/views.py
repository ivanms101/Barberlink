from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response  import Response

from .models import Reserva, DetalleReserva
from .serializers import ReservaSerializer, DetalleReservaSerializer, ProfesionalSerializer, ServicioDisponibleSerializer, ReservaCreateSerializer

from usuarios.models import Usuario
from servicios.models import Servicio

from datetime import datetime

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

HORARIOS_BASE = [
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "14:00",
    "14:30",
    "15:00",
    "15:30",
    "16:00",
    "16:30",
    "17:00",
    "17:30",
    "18:00",
]

@api_view(["GET"])
def horarios_disponibles(request):
    profesional_id = request.GET.get("profesional")
    fecha = request.GET.get("fecha")

    fecha_actual = datetime.now().date()
    hora_actual = datetime.now().time()

    reservas = Reserva.objects.filter(
        barbero_id=profesional_id,
        fecha=fecha
    )

    horas_ocupadas = reservas.values_list("hora", flat=True)

    horarios_disponibles = [
        hora for hora in HORARIOS_BASE
        if hora not in horas_ocupadas
    ]

    if fecha == str(fecha_actual):
        horarios_disponibles = [
            hora for hora in horarios_disponibles
            if datetime.strptime(hora, "%H:%M").time() > hora_actual
        ]

    return Response(horarios_disponibles)

@api_view(["POST"])
def crear_reserva(request):
    servicio_id = request.data.get("servicio")

    if not servicio_id:
        return Response(
            {"error": "Debe seleccionar un servicio"},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        servicio = Servicio.objects.get(
            serv_id=servicio_id,
            serv_activo=True
        )
    except Servicio.DoesNotExist:
        return Response(
            {"error": "El servicio no existe o no esta activo"},
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer = ReservaCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    barbero = serializer.validated_data["barbero"]
    fecha = serializer.validated_data["fecha"]
    hora = serializer.validated_data["hora"]

    if not barbero.usua_activo:
        return Response(
            {"error": "El profesional seleccionado no esta activo"},
            status=status.HTTP_400_BAD_REQUEST
        )
    reserva_existente = Reserva.objects.filter(
        barbero=barbero,
        fecha=fecha,
        hora=hora
    ).exists()

    if reserva_existente:
        return Response(
            {"error": "El horario no esta disponible"},
            status=status.HTTP_400_BAD_REQUEST
        )
    with transaction.atomic():
        reserva = Reserva.objects.create(
            cliente=request.user,
            barbero=barbero,
            fecha=fecha,
            hora=hora,
            estado="PENDIENTE"
        )
        DetalleReserva.objects.create(
            reserva=reserva,
            servicio=servicio
        )
    return Response(
        {
            "mensaje": "Reserva creada",
            "reserva_id": reserva.id
        },
        status=status.HTTP_201_CREATED
    )