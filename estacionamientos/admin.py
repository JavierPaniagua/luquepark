from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import Estacionamiento


@admin.register(Estacionamiento)
class EstacionamientoAdmin(admin.ModelAdmin):
    list_display = (
        "vehiculo",
        "conductor",
        "zona",
        "fecha_inicio",
        "estado",
        "tarifa_aplicada",
        "monto_final",
    )

    list_filter = (
        "estado",
        "zona",
        "fecha_inicio",
    )

    search_fields = (
        "vehiculo__chapa",
        "conductor__username",
        "conductor__first_name",
        "conductor__last_name",
        "zona__nombre",
        "zona__codigo",
    )

    readonly_fields = (
        "estado",
        "fecha_inicio",
        "fecha_fin",
        "tarifa_aplicada",
        "tiempo_utilizado",
        "monto_final",
        "fecha_creacion",
        "fecha_actualizacion",
    )

    list_select_related = (
        "conductor",
        "vehiculo",
        "zona",
    )

    ordering = (
        "-fecha_inicio",
    )

    actions = (
        "finalizar_estacionamientos",
    )

    fieldsets = (
        (
            "Datos del estacionamiento",
            {
                "fields": (
                    "conductor",
                    "vehiculo",
                    "zona",
                    "estado",
                )
            },
        ),
        (
            "Tiempo y tarifa",
            {
                "fields": (
                    "fecha_inicio",
                    "fecha_fin",
                    "tiempo_utilizado",
                    "tarifa_aplicada",
                    "monto_final",
                )
            },
        ),
        (
            "Control",
            {
                "fields": (
                    "fecha_creacion",
                    "fecha_actualizacion",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.action(
        description="Finalizar los estacionamientos seleccionados"
    )
    def finalizar_estacionamientos(self, request, queryset):
        finalizados = 0
        omitidos = 0

        for estacionamiento in queryset:
            try:
                estacionamiento.finalizar()
                finalizados += 1
            except ValidationError:
                omitidos += 1

        if finalizados:
            self.message_user(
                request,
                f"Se finalizaron correctamente {finalizados} estacionamiento(s).",
                level=messages.SUCCESS,
            )

        if omitidos:
            self.message_user(
                request,
                f"Se omitieron {omitidos} estacionamiento(s) porque ya no estaban activos.",
                level=messages.WARNING,
            )