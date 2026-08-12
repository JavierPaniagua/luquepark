from django.contrib import admin

from .forms import ZonaAdminForm
from .models import Zona


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    form = ZonaAdminForm

    change_form_template = (
        "admin/zonas/zona/change_form.html"
    )

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
        "hora_inicio",
        "hora_fin",
    )

    search_fields = (
        "codigo",
        "nombre",
        "descripcion",
    )

    ordering = (
        "nombre",
    )

    fieldsets = (
        (
            "Información de la zona",
            {
                "fields": (
                    "nombre",
                    "codigo",
                    "descripcion",
                    "tarifa_hora",
                    "hora_inicio",
                    "hora_fin",
                    "activa",
                )
            },
        ),
        (
            "Ubicación y mapa",
            {
                "fields": (
                    "latitud",
                    "longitud",
                    "color_mapa",
                    "geometria",
                ),
                "description": (
                    "Use el mapa inferior para dibujar "
                    "las calles o el sector de esta zona."
                ),
            },
        ),
        (
            "Control",
            {
                "fields": (
                    "fecha_creacion",
                    "fecha_actualizacion",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
    )

    readonly_fields = (
        "fecha_creacion",
        "fecha_actualizacion",
    )