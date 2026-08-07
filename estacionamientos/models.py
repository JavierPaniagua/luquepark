from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from decimal import Decimal, ROUND_HALF_UP

from django.utils import timezone
from vehiculos.models import Vehiculo
from zonas.models import Zona


class Estacionamiento(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = "ACTIVO", "Activo"
        FINALIZADO = "FINALIZADO", "Finalizado"
        CANCELADO = "CANCELADO", "Cancelado"

    conductor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="estacionamientos",
    )

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.PROTECT,
        related_name="estacionamientos",
    )

    zona = models.ForeignKey(
        Zona,
        on_delete=models.PROTECT,
        related_name="estacionamientos",
    )

    fecha_inicio = models.DateTimeField(
        auto_now_add=True,
    )

    fecha_fin = models.DateTimeField(
        null=True,
        blank=True,
    )

    estado = models.CharField(
        max_length=15,
        choices=Estado.choices,
        default=Estado.ACTIVO,
        db_index=True,
    )

    # Cantidad total de segundos utilizados.
    tiempo_utilizado = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    # Se copia desde la zona al iniciar el estacionamiento.
    tarifa_aplicada = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    monto_final = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "estacionamiento"
        verbose_name_plural = "estacionamientos"
        ordering = ["-fecha_inicio"]

        constraints = [
            models.UniqueConstraint(
                fields=["vehiculo"],
                condition=Q(estado="ACTIVO"),
                name="vehiculo_con_un_solo_estacionamiento_activo",
            ),
        ]

    def clean(self):
        errores = {}

        if self.conductor_id and not self.conductor.es_conductor:
            errores["conductor"] = (
                "El usuario seleccionado debe tener el rol de conductor."
            )

        if (
            self.conductor_id
            and self.vehiculo_id
            and self.vehiculo.propietario_id != self.conductor_id
        ):
            errores["vehiculo"] = (
                "El vehículo seleccionado no pertenece al conductor."
            )

        if self.zona_id and not self.zona.activa:
            errores["zona"] = (
                "No se puede iniciar un estacionamiento en una zona inactiva."
            )

        if errores:
            raise ValidationError(errores)

    def save(self, *args, **kwargs):
        # Al crear el registro, conservamos la tarifa vigente de la zona.
        if self._state.adding and self.zona_id:
            self.tarifa_aplicada = self.zona.tarifa_hora

        self.full_clean()
        super().save(*args, **kwargs)

    def calcular_monto(self, momento=None):
        """
        Calcula el monto proporcional según los segundos transcurridos.
        Este cálculo siempre se realiza en el servidor.
        """
        if not self.fecha_inicio:
            return Decimal("0.00")

        momento_final = self.fecha_fin or momento or timezone.now()

        segundos = max(
            0,
            int((momento_final - self.fecha_inicio).total_seconds()),
        )

        monto = (
            self.tarifa_aplicada
            * Decimal(segundos)
            / Decimal(3600)
        )

        return monto.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    def finalizar(self):
        """
        Finaliza el estacionamiento y guarda el tiempo y monto definitivo.
        """
        if self.estado != self.Estado.ACTIVO:
            raise ValidationError(
                "Este estacionamiento ya no se encuentra activo."
            )

        self.fecha_fin = timezone.now()

        self.tiempo_utilizado = max(
            0,
            int(
                (
                    self.fecha_fin - self.fecha_inicio
                ).total_seconds()
            ),
        )

        self.monto_final = self.calcular_monto(
            momento=self.fecha_fin
        )

        self.estado = self.Estado.FINALIZADO

        self.save(
            update_fields=[
                "fecha_fin",
                "tiempo_utilizado",
                "monto_final",
                "estado",
                "fecha_actualizacion",
            ]
        )


    def __str__(self):
        return f"{self.vehiculo.chapa} - {self.zona.nombre} - {self.estado}"