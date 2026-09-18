from django.urls import path
from . import views

urlpatterns = [
    path("pagos/", views.pagos, name="pagos"),
    path("reportes/", views.reportes, name="reportes")
]