from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from openpyxl import Workbook

from .models import Pago
from .serializers import PagoSerializer
from reservas.models import Reserva

@login_required
def inicio(request):
    return render(request, "procesos/inicio.html",{"usuario": request.user})

@login_required
def pagos(request):
    return render(request, "procesos/pagos.html")

@login_required
def registrar_pago_pagina(request, id):
    return render(
        request,
        "procesos/registrar_pago.html",
        {
            "pago_id": id
        }
    )

@login_required
def reportes(request):
    return render(request, "procesos/reportes.html")

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["patch"], url_path="registrar")
    def registrar_pago(self, request, pk=None):
        pago = self.get_object()

        metodo = request.data.get("metodo")

        if not metodo:
            return Response(
                {
                    "error":"Debe seleccionar un metodo de pago"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if metodo not in ["EFECTIVO", "TRANSFERENCIA", "TARJETA", "QR"]:
            return Response(
                {"error": "Metodo de pago no valido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        valor = pago.reserva.detalles.all()[0].servicio.serv_tari
        pago.valor = valor
        pago.metodo = metodo
        pago.estado = "PAGADO"
        pago.save()
        return Response(
            {
                "mensaje": "Pago registrado",
                "pago": PagoSerializer(pago).data
            },
            status=status.HTTP_200_OK
        )

@login_required
def exportar_reporte_pagos_excel(request):
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")
    estado = request.GET.get("estado")

    pagos = Pago.objects.all().select_related(
        "reserva",
        "reserva__cliente",
        "reserva__barbero"
    )

    if fecha_inicio:
        pagos = pagos.filter(reserva__fecha__gte=fecha_inicio)
    if fecha_fin:
        pagos = pagos.filter(reserva__fecha__lte=fecha_fin)
    if estado and estado != "TODOS":
        pagos = pagos.filter(estado=estado)
    pagos = pagos.order_by(
        "reserva__fecha",
        "reserva__hora"
    )
    libro = Workbook()
    hoja = libro.active
    hoja.title = "Reporte de ventas"

    hoja.append([
        "Reserva",
        "Cliente",
        "Barbero",
        "Servicio",
        "Fecha",
        "Hora",
        "valor",
        "Estado"
    ])

    total = 0

    for pago in pagos:
        detalle = pago.reserva.detalles.select_related("servicio").first()
        servicio = ""
        valor = 0

        if detalle:
            servicio = detalle.servicio.serv_nomb
            valor = detalle.servicio.serv_tari

        hoja.append([
            pago.reserva.id,
            pago.reserva.cliente.usua_nomb,
            pago.reserva.barbero.usua_nomb,
            servicio,
            pago.reserva.fecha,
            pago.reserva.hora,
            valor,
            pago.estado
        ])

        if pago.estado == "PAGADO":
            total += float(valor)
    hoja.append([])
    hoja.append([
        "",
        "",
        "",
        "",
        "",
        "Total recaudado",
        total,
        ""
    ])
    respuesta = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    respuesta["Content-Disposition"]=(
        'attachment; filename="reporte_ventas.xlsx"'
    )
    libro.save(respuesta)
    return respuesta

@login_required
def exportar_reporte_citas_excel(request):
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")
    estado = request.GET.get("estado")

    reservas = Reserva.objects.all().select_related(
        "cliente",
        "barbero"
    )

    if fecha_inicio:
        reservas = reservas.filter(
            fecha__gte=fecha_inicio
        )

    if fecha_fin:
        reservas = reservas.filter(
            fecha__lte=fecha_fin
        )

    if estado and estado != "TODOS":
        reservas = reservas.filter(
            estado=estado
        )

    reservas = reservas.order_by(
        "fecha",
        "hora"
    )

    libro = Workbook()
    hoja = libro.active
    hoja.title = "Reporte de citas"

    hoja.append([
        "Reserva",
        "Cliente",
        "Barbero",
        "Servicio",
        "Fecha",
        "Hora",
        "Estado"
    ])

    for reserva in reservas:
        detalle = reserva.detalles.select_related(
            "servicio"
        ).first()

        servicio = ""

        if detalle:
            servicio = detalle.servicio.serv_nomb

        hoja.append([
            reserva.id,
            reserva.cliente.usua_nomb,
            reserva.barbero.usua_nomb,
            servicio,
            reserva.fecha,
            reserva.hora,
            reserva.estado
        ])

    respuesta = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    respuesta["Content-Disposition"] = (
        'attachment; filename="reporte_citas.xlsx"'
    )

    libro.save(respuesta)

    return respuesta