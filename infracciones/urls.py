from django.urls import path

from . import views


app_name = "infracciones"

urlpatterns = [
    path(
        "registrar/<str:chapa>/",
        views.registrar_infraccion,
        name="registrar",
    ),
]