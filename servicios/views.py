from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Servicio
from usuarios.permissions import IsAdminRole
from .serializers import ServicioSerializer

@login_required
def servicios(request):
    if request.user.usua_rol.rol_nomb != "admin":
        return HttpResponse("No tiene acceso a esta funcion")
    return render(request, "servicios/servicios.html")

class ServicioViewSet(viewsets.ModelViewSet):
    http_method_names =["get", "post", "patch", "head", "options"]
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@login_required
def crear_servicio(request):
    if request.user.usua_rol.rol_nomb != "admin":
        return HttpResponse("No tiene acceso a esta funcion")
    return render(request, "servicios/crear_servicio.html")

@login_required
def editar_servico(request,pk):
    if request.user.usua_rol.rol_nomb != "admin":
        return HttpResponse("No tiene accseso a esta funcion")
    return render(
        request,
        "servicios/editar_servicio.html",
        {"pk":pk}
    )