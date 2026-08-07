from django.urls import path

from . import views


app_name = "usuarios"

urlpatterns = [
    path(
        "",
        views.iniciar_sesion,
        name="inicio",
    ),

    path(
        "login/",
        views.iniciar_sesion,
        name="login",
    ),

    path(
        "registro/",
        views.registrar_conductor,
        name="registro",
    ),

    path(
        "logout/",
        views.cerrar_sesion,
        name="logout",
    ),

    path(
    "service-worker.js",
    views.service_worker,
    name="service_worker",
),
]