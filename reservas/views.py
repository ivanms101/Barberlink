from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response  import Response

from .models import Reserva, DetalleReserva
from .serializers import ReservaSerializer, DetalleReservaSerializer, ProfesionalSerializer, ServicioDisponibleSerializer, ReservaCreateSerializer, UsuarioReservaSerializer

from usuarios.models import Usuario
from servicios.models import Servicio
from gestion.models import HorarioDia, HorarioFranja

from datetime import datetime, timedelta

@login_required
def reservas(request):
    return render(
        request,
        "reservas/reservas.html",
        {
            "rol_usuario": request.user.usua_rol.rol_nomb
        }
    )

@login_required
def crear_reserva_pagina(request):
    return render(request, "reservas/crear_reserva.html")

@login_required
def agendar_reserva_pagina(request):
    return render(request, "reservas/agendar_reserva.html")

class ReservaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        rol = usuario.usua_rol.rol_nomb

        if rol in ["admin", "manage", "assist"]:
            return Reserva.objects.all()
        if rol == "empl":
            return Reserva.objects.filter(barbero=usuario, estado="PENDIENTE")
        if rol == "usua":
            return Reserva.objects.filter(cliente=usuario)
        return Reserva.objects.none()
    @action(detail=True, methods=["patch"])
    def cancelar(self, request, pk=None):
        reserva = self.get_object()
        rol = request.user.usua_rol.rol_nomb

        if rol == "empl":
            return Response(
                {"error": "El barbero no puede cancelar reservas"},
                status=status.HTTP_403_FORBIDDEN
            )
        if reserva.estado != "PENDIENTE":
            return Response(
                {"error": "Solo se pueden cancelar reservas pendientes"},
                status=status.HTTP_400_BAD_REQUEST
            )
        reserva.estado = "CANCELADA"
        reserva.save(update_fields=["estado"])
        return Response(
            {"mensaje": "Resverva cancelada correctamente", "reserva_id": reserva.id},
            status=status.HTTP_200_OK
        )
    @action(detail=True, methods=["patch"])
    def finalizar(self, request, pk=None):
        reserva = self.get_object()
        rol = request.user.usua_rol.rol_nomb

        if rol not in ["admin", "manage", "assist"]:
            return Response(
            {"error": "No tiene permisos para finalizar reservas"},
            status=status.HTTP_403_FORBIDDEN
            )

        if reserva.estado != "PENDIENTE":
            return Response(
            {"error": "Solo se pueden finalizar reservas pendientes"},
            status=status.HTTP_400_BAD_REQUEST
        )

        reserva.estado = "FINALIZADA"
        reserva.save(update_fields=["estado"])

        return Response(
            {
                "mensaje": "Reserva finalizada correctamente",
                "reserva_id": reserva.id
            },
        status=status.HTTP_200_OK
    )
    
    @action(detail=True, methods=["patch"])
    def reagendar(self, request, pk=None):
        reserva = self.get_object()
        usuario = request.user
        rol = usuario.usua_rol.rol_nomb

        if rol == "empl":
            return Response(
                {"error": "El barbero no puede reagendar reservas"},
                status=status.HTTP_403_FORBIDDEN
            )
        if reserva.estado != "PENDIENTE":
            return Response(
                {"error": "Solo se pueden reagendar reservas pendientes"},
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
                {"error": "El profesional no esta activo"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if barbero.usua_rol.rol_nomb != "empl":
            return Response(
                {"error": "El usuario seleccionado no es una barbero"},
                status=status.HTTP_400_BAD_REQUEST
            )
        fecha_actual = datetime.now().date()

        if fecha < fecha_actual:
            return Response(
                {"error": "No se puede reagendar para una fecha pasada"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            hora_reserva = datetime.strptime(hora, "%H:%M").time()
        except ValueError:
            return Response(
                {"error": "La hora no tiene un formato valido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        detalle = reserva.detalles.first()

        if detalle is None:
            return Response(
                {"error": "La reserva no tiene un servicio asociado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        servicio = detalle.servicio

        horarios = obtener_horarios_disponibles(
            barbero.usua_id,
            fecha,
            servicio,
            reserva_excluir_id=reserva.id
        )

        if fecha == fecha_actual:
            fecha_hora_reserva = datetime.combine(fecha, hora_reserva)
            if fecha_hora_reserva <= datetime.now():
                return Response(
                    {"error": "No se puede reagendar para una hora pasada"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if hora not in horarios:
            return Response(
                {"error": "El horario no esta disponible"},
                status=status.HTTP_400_BAD_REQUEST
            )
        with transaction.atomic():
            reserva.barbero = barbero
            reserva.fecha = fecha
            reserva.hora = hora
            reserva.save(
                update_fields=[
                    "barbero",
                    "fecha",
                    "hora"
                ]
            )
        return Response(
            {"mensaje": "Reserva reagendada correctamente", "reserva_id": reserva.id},
            status=status.HTTP_200_OK
        )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def clientes_disponibles(request):

    rol = request.user.usua_rol.rol_nomb

    if rol not in ["admin", "manage", "assist"]:
        return Response(
            {"error": "No tiene permisos para consultar clientes"},
            status=status.HTTP_403_FORBIDDEN
        )

    clientes = Usuario.objects.filter(
        usua_activo=True,
        usua_rol__rol_nomb="usua"
    ).order_by("usua_nomb")

    serializer = UsuarioReservaSerializer(
        clientes,
        many=True
    )

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profesionales(request):
    profesionales = Usuario.objects.filter(
        usua_activo = True,
        usua_rol__rol_nomb = "empl"
    )
    serializer = ProfesionalSerializer(profesionales, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def servicios_disponibles(request):
    servicios = Servicio.objects.filter(
        serv_activo = True
    )
    serializer = ServicioDisponibleSerializer(servicios, many=True)
    return Response(serializer.data)

def obtener_horarios_disponibles(profesional_id, fecha_reserva, servicio, reserva_excluir_id=None):
    dia_semana = fecha_reserva.isoweekday()

    try:
        horario_dia = HorarioDia.objects.get(
            hord_dia=dia_semana,
            hord_activo=True
        )
    except HorarioDia.DoesNotExist:
        return []

    franjas = HorarioFranja.objects.filter(
        hord=horario_dia,
        horf_activo=True
    ).order_by("horf_hora_inicio")

    reservas = Reserva.objects.filter(
        barbero_id=profesional_id,
        fecha=fecha_reserva
    ).exclude(
        estado="CANCELADA"
    )

    if reserva_excluir_id is not None:
        reservas = reservas.exclude(id=reserva_excluir_id)

    horarios_disponibles = []

    for franja in franjas:

        hora_inicio = datetime.combine(
            fecha_reserva,
            franja.horf_hora_inicio
        )

        hora_fin_franja = datetime.combine(
            fecha_reserva,
            franja.horf_hora_fin
        )

        while True:

            hora_fin_reserva = hora_inicio + timedelta(
                minutes=servicio.serv_duracion
            )

            if hora_fin_reserva > hora_fin_franja:
                break

            horario_ocupado = False

            for reserva in reservas:

                inicio_reserva = datetime.combine(
                    fecha_reserva,
                    datetime.strptime(
                        reserva.hora,
                        "%H:%M"
                    ).time()
                )

                detalles = reserva.detalles.all()

                duracion_reserva = sum(
                    detalle.servicio.serv_duracion
                    for detalle in detalles
                )

                fin_reserva = inicio_reserva + timedelta(
                    minutes=duracion_reserva
                )

                if (
                    hora_inicio < fin_reserva
                    and hora_fin_reserva > inicio_reserva
                ):
                    horario_ocupado = True
                    break

            if not horario_ocupado:
                horarios_disponibles.append(
                    hora_inicio.strftime("%H:%M")
                )

            hora_inicio += timedelta(minutes=15)

    return horarios_disponibles

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def horarios_disponibles(request):

    profesional_id = request.GET.get("profesional")
    fecha = request.GET.get("fecha")
    servicio_id = request.GET.get("servicio")
    reserva_excluir_id = request.GET.get("reserva_excluir")

    if not profesional_id or not fecha or not servicio_id:
        return Response(
            {"error": "Debe indicar un profesional, fecha y servicio"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        fecha_reserva = datetime.strptime(
            fecha,
            "%Y-%m-%d"
        ).date()
    except ValueError:
        return Response(
            {"error": "La fecha no tiene un formato valido"},
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

    horarios = obtener_horarios_disponibles(
        profesional_id,
        fecha_reserva,
        servicio,
        reserva_excluir_id=reserva_excluir_id
    )

    fecha_actual = datetime.now().date()
    hora_actual = datetime.now()

    if fecha_reserva == fecha_actual:
        horarios = [
            hora
            for hora in horarios
            if datetime.combine(
                fecha_reserva,
                datetime.strptime(hora, "%H:%M").time()
            ) > hora_actual
        ]

    return Response(horarios)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def crear_reserva(request):

    usuario = request.user
    rol = usuario.usua_rol.rol_nomb

    if rol not in ["admin", "manage", "assist", "usua"]:
        return Response(
            {"error": "No tiene permisos para crear reservas"},
            status=status.HTTP_403_FORBIDDEN
        )

    # Determinar el cliente de la reserva
    cliente_id = request.data.get("cliente")

    if not cliente_id:

        # Mantiene funcionando el formulario actual
        cliente = usuario

    else:

        # Solo estos roles pueden seleccionar otro cliente
        if rol not in ["admin", "manage", "assist"]:
            return Response(
                {"error": "No tiene permisos para seleccionar otro cliente"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            cliente = Usuario.objects.select_related(
                "usua_rol"
            ).get(
                usua_id=cliente_id
            )
        except Usuario.DoesNotExist:
            return Response(
                {"error": "El cliente seleccionado no existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not cliente.usua_activo:
            return Response(
                {"error": "El cliente seleccionado no esta activo"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if cliente.usua_rol.rol_nomb != "usua":
            return Response(
                {"error": "El usuario seleccionado no es un cliente"},
                status=status.HTTP_400_BAD_REQUEST
            )

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

    serializer = ReservaCreateSerializer(
        data=request.data
    )

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

    if barbero.usua_rol.rol_nomb != "empl":
        return Response(
            {"error": "El profesional seleccionado no es un barbero"},
            status=status.HTTP_400_BAD_REQUEST
        )

    fecha_actual = datetime.now().date()

    if fecha < fecha_actual:
        return Response(
            {"error": "No se puede crear una reserva para una fecha pasada"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        hora_reserva = datetime.strptime(
            hora,
            "%H:%M"
        ).time()
    except ValueError:
        return Response(
            {"error": "La hora no tiene un formato valido"},
            status=status.HTTP_400_BAD_REQUEST
        )

    horarios = obtener_horarios_disponibles(
        barbero.usua_id,
        fecha,
        servicio
    )

    if fecha == fecha_actual:

        fecha_hora_reserva = datetime.combine(
            fecha,
            hora_reserva
        )

        if fecha_hora_reserva <= datetime.now():
            return Response(
                {"error": "No se puede crear una reserva en una hora pasada"},
                status=status.HTTP_400_BAD_REQUEST
            )

    if hora not in horarios:
        return Response(
            {"error": "El horario no esta disponible"},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():

        reserva = Reserva.objects.create(
            cliente=cliente,
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