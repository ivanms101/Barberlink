from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Usuario

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