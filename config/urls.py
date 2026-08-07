from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "",
        include("usuarios.urls"),
    ),

    path(
        "vehiculos/",
        include("vehiculos.urls"),
    ),

    path(
        "zonas/",
        include("zonas.urls"),
    ),

    path(
        "estacionamientos/",
        include("estacionamientos.urls"),
    ),
]