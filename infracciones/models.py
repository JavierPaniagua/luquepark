import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from vehiculos.models import Vehiculo
from zonas.models import Zona


class Infraccion(models.Model):
    class Motivo(models.TextChoices):
        SIN_ESTACIONAMIENTO = (
            "SIN_ESTACIONAMIENTO",
            "Sin estacionamiento activo",
        )

        ZONA_INCORRECTA = (
            "ZONA_INCORRECTA",
            "Estacionamiento en zona incorrecta",
        )

        OTRO = (
            "OTRO",
            "Otro",
        )

    class Estado(models.TextChoices):
        PENDIENTE = (
            "PENDIENTE",
            "Pendiente",
        )

        ANULADA = (
            "ANULADA",
            "Anulada",
        )

    inspector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="infracciones_registradas",
    )

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="infracciones",
    )

    chapa = models.CharField(
        max_length=15,
        db_index=True,
    )

    zona = models.ForeignKey(
        Zona,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="infracciones",
    )

    motivo = models.CharField(
        max_length=30,
        choices=Motivo.choices,
        default=Motivo.SIN_ESTACIONAMIENTO,
    )

    observaciones = models.TextField(
        blank=True,
    )

    estado = models.CharField(
        max_length=15,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
        db_index=True,
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "infracción"
        verbose_name_plural = "infracciones"
        ordering = ["-fecha_registro"]

    def clean(self):
        if self.inspector_id and not self.inspector.es_inspector:
            raise ValidationError(
                {
                    "inspector": (
                        "El usuario seleccionado debe tener "
                        "el rol de inspector."
                    )
                }
            )

    def save(self, *args, **kwargs):
        if self.vehiculo_id:
            self.chapa = self.vehiculo.chapa
        else:
            self.chapa = re.sub(
                r"[^A-Za-z0-9]",
                "",
                self.chapa,
            ).upper()

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.chapa} - "
            f"{self.get_motivo_display()} - "
            f"{self.fecha_registro:%d/%m/%Y %H:%M}"
        )