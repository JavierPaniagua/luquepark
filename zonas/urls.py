from django.urls import path

from . import views


app_name = "zonas"

urlpatterns = [
    path(
        "mapa/",
        views.mapa_zonas,
        name="mapa",
    ),
]