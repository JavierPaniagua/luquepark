from django.contrib import admin

from .models import Zona


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "tarifa_hora",
        "hora_inicio",
        "hora_fin",
        "activa",
    )

    list_filter = (
        "activa",
    )

    search_fields = (
        "codigo",
        "nombre",
        "descripcion",
    )

    ordering = (
        "nombre",
    )

    readonly_fields = (
        "fecha_creacion",
        "fecha_actualizacion",
    )

    fieldsets = (
        (
            "Datos principales",
            {
                "fields": (
                    "nombre",
                    "codigo",
                    "descripcion",
                    "activa",
                )
            },
        ),
        (
            "Tarifa y horario",
            {
                "fields": (
                    "tarifa_hora",
                    "hora_inicio",
                    "hora_fin",
                )
            },
        ),
        (
            "Ubicación en el mapa",
            {
                "fields": (
                    "latitud",
                    "longitud",
                )
            },
        ),
        (
            "Información del sistema",
            {
                "fields": (
                    "fecha_creacion",
                    "fecha_actualizacion",
                ),
                "classes": ("collapse",),
            },
        ),
    )