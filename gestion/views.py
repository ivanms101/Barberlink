from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Auditoria, HorarioDia, HorarioFranja
from .serializers import AuditoriaSerializer, HorarioDiaSerializer, HorarioFranjaSerializer
from usuarios.permissions import IsAdminRole

@login_required
def configuracion(request):
    return render(request, "gestion/configuracion.html")

@login_required
def auditoria(request):
    if request.user.usua_rol.rol_nomb != "admin":
        return HttpResponse("No tiene acceso a esa funcion")
    return render(request, "gestion/auditoria.html")

class AuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Auditoria.objects.all().order_by("-fecha")
    serializer_class = AuditoriaSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

class HorarioDiaViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "head", "options"]

    queryset = HorarioDia.objects.all().order_by("hord_dia")
    serializer_class = HorarioDiaSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

class HorarioFranjaViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    queryset = HorarioFranja.objects.all().order_by("hord_id", "horf_hora_inicio")
    serializer_class = HorarioFranjaSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

