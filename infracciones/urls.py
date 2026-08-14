from django.urls import path

from . import views


app_name = "infracciones"

urlpatterns = [
    path(
        "registrar/<str:chapa>/",
        views.registrar_infraccion,
        name="registrar",
    ),

    path(
    "mis-infracciones/",
    views.mis_infracciones,
    name="mis_infracciones",
),
]