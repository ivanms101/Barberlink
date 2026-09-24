from django.urls import path, include
from . import views
from procesos import views as procesos_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("api/usuarios", views.UsuarioViewSet, basename="usuarios")

urlpatterns =[
    path("prueba/", views.prueba, name="prueba"),
    path("login/", views.login_view, name="login"),
    path("inicio/", procesos_views.inicio, name="inicio"),
    path("logout/", views.logout_view, name="logout"),
    path("administracion/", views.administracion, name="administracion"),
    path("usuarios/", views.usuarios, name="usuarios"),
    path("usuarios/crear/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/editar/<int:pk>/", views.editar_usuario, name="editar_usuario"),
    path("usuarios/password/<int:pk>/", views.cambiar_password, name="cambiar_password"),
    path("", include(router.urls)),
]