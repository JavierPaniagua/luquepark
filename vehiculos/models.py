from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Vehiculo(models.Model):
    class TipoVehiculo(models.TextChoices):
        AUTOMOVIL = "AUTOMOVIL", "Automóvil"
        CAMIONETA = "CAMIONETA", "Camioneta"
        MOTOCICLETA = "MOTOCICLETA", "Motocicleta"
        OTRO = "OTRO", "Otro"

    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vehiculos",
        verbose_name="Propietario",
    )

    chapa = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Número de chapa",
        help_text="Ejemplo: ABCD123",
    )

    tipo = models.CharField(
        max_length=20,
        choices=TipoVehiculo.choices,
        default=TipoVehiculo.AUTOMOVIL,
        verbose_name="Tipo de vehículo",
    )

    marca = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Marca",
    )

    modelo = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Modelo",
    )

    color = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Color",
    )

    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de registro",
    )

    def clean(self):
        super().clean()

        if self.propietario_id and not self.propietario.es_conductor:
            raise ValidationError(
                {
                    "propietario": (
                        "El propietario del vehículo debe tener el rol Conductor."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.chapa = self.chapa.replace(" ", "").replace("-", "").upper()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.chapa} - {self.propietario}"

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ["chapa"]