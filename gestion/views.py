from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Auditoria
from .serializers import AuditoriaSerializer
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

