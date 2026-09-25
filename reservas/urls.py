from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    "api/reservas",
    views.ReservaViewSet,
    basename="reservas"
)

urlpatterns = [
    path("", views.reservas, name="reservas"),
    path("api/profesionales/", views.profesionales, name="profesionales"),
    path("api/servicios-disponibles/", views.servicios_disponibles, name="servicios_disponibles"),
    path("", include(router.urls)),
]