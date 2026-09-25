from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("api/servicios", views.ServicioViewSet, basename="servicios")

urlpatterns = [
    path("",views.servicios, name="servicios"),
    path("crear/", views.crear_servicio, name="crear_servicio"),
    path("editar/<int:pk>/", views.editar_servico, name="editar_servicio"),
    path("",include(router.urls)),
]