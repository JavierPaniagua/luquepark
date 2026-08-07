from django.contrib import admin

from .models import Infraccion


@admin.register(Infraccion)
class InfraccionAdmin(admin.ModelAdmin):
    list_display = (
        "chapa",
        "inspector",
        "zona",
        "motivo",
        "estado",
        "fecha_registro",
    )

    list_filter = (
        "estado",
        "motivo",
        "zona",
        "fecha_registro",
    )

    search_fields = (
        "chapa",
        "inspector__username",
        "inspector__first_name",
        "inspector__last_name",
        "vehiculo__chapa",
        "observaciones",
    )

    readonly_fields = (
        "fecha_registro",
        "fecha_actualizacion",
    )

    list_select_related = (
        "inspector",
        "vehiculo",
        "zona",
    )

    ordering = (
        "-fecha_registro",
    )

    fieldsets = (
        (
            "Datos de la infracción",
            {
                "fields": (
                    "inspector",
                    "vehiculo",
                    "chapa",
                    "zona",
                    "motivo",
                    "observaciones",
                    "estado",
                )
            },
        ),
        (
            "Control",
            {
                "fields": (
                    "fecha_registro",
                    "fecha_actualizacion",
                ),
                "classes": ("collapse",),
            },
        ),
    )