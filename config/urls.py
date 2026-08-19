from django.contrib import admin
from django.urls import include, path


admin.site.site_header = (
    "Administración LuquePark"
)

admin.site.site_title = (
    "LuquePark"
)

admin.site.index_title = (
    "Panel de administración"
)


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

    path(
        "infracciones/",
        include("infracciones.urls"),
    ),
]