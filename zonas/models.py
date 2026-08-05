from django.core.validators import MinValueValidator
from django.db import models


class Zona(models.Model):
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre de la zona",
    )

    codigo = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Código",
        help_text="Ejemplo: CEN, MER o HOS",
    )

    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    tarifa_hora = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Tarifa por hora",
        help_text="Monto en guaraníes",
    )

    hora_inicio = models.TimeField(
        verbose_name="Hora de inicio",
    )

    hora_fin = models.TimeField(
        verbose_name="Hora de finalización",
    )

    latitud = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        verbose_name="Latitud",
    )

    longitud = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        verbose_name="Longitud",
    )

    activa = models.BooleanField(
        default=True,
        verbose_name="Zona activa",
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización",
    )

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Zona"
        verbose_name_plural = "Zonas"
        ordering = ["nombre"]