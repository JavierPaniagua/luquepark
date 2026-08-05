from django.contrib import admin

from .models import Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = (
        "chapa",
        "propietario",
        "tipo",
        "marca",
        "modelo",
        "color",
        "activo",
    )

    list_filter = (
        "tipo",
        "activo",
    )

    search_fields = (
        "chapa",
        "marca",
        "modelo",
        "color",
        "propietario__username",
        "propietario__first_name",
        "propietario__last_name",
        "propietario__cedula",
    )

    ordering = (
        "chapa",
    )

    autocomplete_fields = (
        "propietario",
    )

    readonly_fields = (
        "fecha_registro",
    )

    fieldsets = (
        (
            "Propietario",
            {
                "fields": (
                    "propietario",
                )
            },
        ),
        (
            "Datos del vehículo",
            {
                "fields": (
                    "chapa",
                    "tipo",
                    "marca",
                    "modelo",
                    "color",
                    "activo",
                )
            },
        ),
        (
            "Información del sistema",
            {
                "fields": (
                    "fecha_registro",
                ),
                "classes": ("collapse",),
            },
        ),
    )