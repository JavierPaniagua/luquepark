from django.urls import path

from . import views


app_name = "vehiculos"

urlpatterns = [
    path(
        "",
        views.mis_vehiculos,
        name="mis_vehiculos",
    ),

    path(
        "registrar/",
        views.registrar_vehiculo,
        name="registrar",
    ),
]