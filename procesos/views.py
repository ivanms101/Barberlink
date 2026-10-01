from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Pago
from .serializers import PagoSerializer

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