from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        CONDUCTOR = "CONDUCTOR", "Conductor"
        INSPECTOR = "INSPECTOR", "Inspector"

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.CONDUCTOR,
        verbose_name="Rol",
    )

    cedula = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Cédula",
    )

    telefono = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Teléfono",
    )

    @property
    def es_administrador(self):
        return self.rol == self.Rol.ADMINISTRADOR or self.is_superuser

    @property
    def es_conductor(self):
        return self.rol == self.Rol.CONDUCTOR

    @property
    def es_inspector(self):
        return self.rol == self.Rol.INSPECTOR

    def __str__(self):
        nombre_completo = self.get_full_name().strip()
        return nombre_completo or self.username