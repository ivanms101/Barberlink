from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Usuario, Rol
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminRole
from .serializers import UsuarioSerializer, UsuarioCreateSerializer, UsuarioPasswordSerializer, UsuarioEstadoSerializer

def prueba(request):
    return HttpResponse(request.method)

def login_view(request):
    if request.method == "POST":
        documento = request.POST.get("documento")
        password = request.POST.get("password")

        usuario = authenticate(
            usua_doc_id = documento,
            password = password
        )
        if usuario is not None:
            login(request, usuario)
            return redirect("inicio")
        return render(request, "usuarios/login.html", {"error":"Documento o contraseña incorrectos"})
    return render(request, "usuarios/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def administracion(request):
    if request.user.usua_rol.rol_nomb == "admin":
        return HttpResponse("Panel de administracion")
    else:
        return HttpResponse("No tiene acceso a esta funcion")

@login_required
def usuarios(request):
    if request.user.usua_rol.rol_nomb != "admin":
        return HttpResponse("No tiene acceso a esa funcion")
    return render(request, "usuarios/usuarios.html", {"usuarios":usuarios})

@login_required
def crear_usuario(request):
    if request.user.usua_rol.rol_nomb != "admin":
        return HttpResponse("No tiene acceso a esa funcion")
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        tipo_documento = request.POST.get("tipo_documento")
        documento = request.POST.get("documento")
        telefono = request.POST.get("telefono")
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        rol_id = request.POST.get("rol")

        rol = Rol.objects.get(rol_id=rol_id)

        usuario = Usuario.objects.create_user(
            usua_doc_id = documento,
            password = password,
            usua_nomb = nombre,
            usua_rol = rol,
            usua_tp_doc = tipo_documento,
            usua_tel = telefono,
            usua_cor = correo
        )
        return redirect("usuarios")
    roles = Rol.objects.all()
    return render(request, "usuarios/crear_usuario.html", {"roles":roles})

class UsuarioViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "head", "options"]
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_serializer_class(self):
        if self.action == "create":
            return UsuarioCreateSerializer
        return UsuarioSerializer

    @action(detail=True, methods=["post"], url_path="password")
    def cambiar_password(self, request, pk=None):
        usuario = self.get_object()
        serializer = UsuarioPasswordSerializer(data=request.data)

        if serializer.is_valid():
            usuario.set_password(serializer.validated_data["password"])
            usuario.save()
            return Response({"detail":"Contraseña actualizada."})
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=["patch"], url_path="estado")
    def cambiar_estado(self, request, pk=None):
        usuario = self.get_object()
        serializer = UsuarioEstadoSerializer(data=request.data)

        if serializer.is_valid():
            usuario.usua_activo = serializer.validated_data["usua_activo"]
            usuario.save()
            return Response({"detail":"Estado actualizado"})
        return Response(serializer.errors, status=400)

@login_required
def editar_usuario(request, pk):
    if request.user.usua_rol.rol_nomb !="admin":
        return HttpResponse("No tiene acceso a esta funcion")

    roles = Rol.objects.all()

    return render(request, "usuarios/editar_usuario.html",{"roles": roles, "pk": pk})

@login_required
def cambiar_password(request, pk):
    if request.user.usua_rol.rol_nomb !="admin":
        return HttpResponse("No tiene acceso a esta funcion")
    return render(request, "usuarios/cambiar_password.html",{"pk":pk})