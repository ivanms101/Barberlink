from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def inicio(request):
    return render(request, "procesos/inicio.html",{"usuario": request.user})

@login_required
def pagos(request):
    return render(request, "procesos/pagos.html")

@login_required
def reportes(request):
    return render(request, "procesos/reportes.html")