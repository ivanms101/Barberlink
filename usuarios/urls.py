from django.urls import path
from . import views
from procesos import views as procesos_views

urlpatterns =[
    path("prueba/", views.prueba, name="prueba"),
    path("login/", views.login_view, name="login"),
    path("inicio/", procesos_views.inicio, name="inicio"),
    path("logout/", views.logout_view, name="logout"),
    path("administracion/", views.administracion, name="administracion"),
    path("usuarios/", views.usuarios, name="usuarios"),
]