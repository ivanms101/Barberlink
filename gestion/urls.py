from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("api/auditoria", views.AuditoriaViewSet, basename="auditoria")
router.register("api/horarios-dias", views.HorarioDiaViewSet, basename="horarios-dias")
router.register("api/horarios-franjas", views.HorarioFranjaViewSet, basename="horarios-franjas")

urlpatterns = [
    path("", views.configuracion, name="configuracion"),
    path("auditoria/", views.auditoria, name="auditoria"),
    path("", include(router.urls)),
]