from django.urls import path

from . import views


app_name = "estacionamientos"

urlpatterns = [

    path(
    "panel/",
    views.panel_conductor,
    name="panel_conductor",
),

    path(
        "iniciar/",
        views.iniciar_estacionamiento,
        name="iniciar",
    ),

    path(
        "activos/",
        views.estacionamientos_activos,
        name="activos",
    ),

    path(
        "historial/",
        views.historial_estacionamientos,
        name="historial",
    ),

    path(
        "<int:estacionamiento_id>/finalizar/",
        views.finalizar_estacionamiento,
        name="finalizar",
    ),

    path(
        "inspector/verificar-chapa/",
        views.verificar_chapa,
        name="verificar_chapa",
    ),

    path(
    "admin/reporte/",
    views.reporte_general,
    name="reporte_general",
),
]