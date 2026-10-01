from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("api/pagos", views.PagoViewSet, basename="pagos")

urlpatterns = [
    path("pagos/", views.pagos, name="pagos"),
    path("pagos/registrar/<int:id>/", views.registrar_pago_pagina, name="registrar_pago_pagina"),
    path("reportes/", views.reportes, name="reportes"),
    path("", include(router.urls)),
]