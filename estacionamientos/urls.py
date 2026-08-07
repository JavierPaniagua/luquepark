from django.urls import path

from . import views


app_name = "estacionamientos"

urlpatterns = [
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
        "<int:estacionamiento_id>/finalizar/",
        views.finalizar_estacionamiento,
        name="finalizar",
    ),

    path(
        "inspector/verificar-chapa/",
        views.verificar_chapa,
        name="verificar_chapa",
    ),
]