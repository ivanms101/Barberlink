from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Usuario, Rol

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
        return HttpResponse("Credenciales incorrectas")
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
    usuarios = Usuario.objects.all()
    return render(request, "usuarios/usuarios.html", {"usuarios":usuarios})

@login_required
def crear_usuario(request):
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