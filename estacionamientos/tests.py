from datetime import time, timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from vehiculos.models import Vehiculo
from zonas.models import Zona

from .models import Estacionamiento


Usuario = get_user_model()


class EstacionamientoModelTest(TestCase):
    def setUp(self):
        self.conductor = Usuario.objects.create_user(
            username="conductor_prueba",
            password="clave-segura-123",
            first_name="Conductor",
            last_name="Prueba",
            rol="CONDUCTOR",
        )

        self.otro_conductor = Usuario.objects.create_user(
            username="otro_conductor",
            password="clave-segura-456",
            first_name="Otro",
            last_name="Conductor",
            rol="CONDUCTOR",
        )

        self.zona = Zona.objects.create(
            nombre="Zona de prueba",
            codigo="PRU",
            descripcion="Zona para pruebas automáticas",
            tarifa_hora=Decimal("5000.00"),
            hora_inicio=time(7, 0),
            hora_fin=time(18, 0),
            latitud=Decimal("-25.267000"),
            longitud=Decimal("-57.487000"),
            activa=True,
        )

        self.tipo_vehiculo = (
            Vehiculo._meta
            .get_field("tipo")
            .choices[0][0]
        )

        self.vehiculo = Vehiculo.objects.create(
            propietario=self.conductor,
            chapa="TEST001",
            tipo=self.tipo_vehiculo,
            marca="Marca prueba",
            modelo="Modelo prueba",
            color="Blanco",
            activo=True,
        )

        self.vehiculo_ajeno = Vehiculo.objects.create(
            propietario=self.otro_conductor,
            chapa="TEST002",
            tipo=self.tipo_vehiculo,
            marca="Otra marca",
            modelo="Otro modelo",
            color="Negro",
            activo=True,
        )

    def test_copia_tarifa_de_la_zona_al_iniciar(self):
        estacionamiento = Estacionamiento.objects.create(
            conductor=self.conductor,
            vehiculo=self.vehiculo,
            zona=self.zona,
        )

        self.assertEqual(
            estacionamiento.tarifa_aplicada,
            Decimal("5000.00"),
        )

        self.assertEqual(
            estacionamiento.estado,
            Estacionamiento.Estado.ACTIVO,
        )

    def test_impide_dos_estacionamientos_activos(self):
        Estacionamiento.objects.create(
            conductor=self.conductor,
            vehiculo=self.vehiculo,
            zona=self.zona,
        )

        segundo_estacionamiento = Estacionamiento(
            conductor=self.conductor,
            vehiculo=self.vehiculo,
            zona=self.zona,
        )

        with self.assertRaises(ValidationError):
            segundo_estacionamiento.save()

    def test_impide_usar_vehiculo_de_otro_conductor(self):
        estacionamiento = Estacionamiento(
            conductor=self.conductor,
            vehiculo=self.vehiculo_ajeno,
            zona=self.zona,
        )

        with self.assertRaises(ValidationError):
            estacionamiento.save()

    def test_calcula_una_hora_de_estacionamiento(self):
        estacionamiento = Estacionamiento.objects.create(
            conductor=self.conductor,
            vehiculo=self.vehiculo,
            zona=self.zona,
        )

        momento_fin = timezone.now()
        momento_inicio = momento_fin - timedelta(hours=1)

        Estacionamiento.objects.filter(
            id=estacionamiento.id,
        ).update(
            fecha_inicio=momento_inicio,
        )

        estacionamiento.refresh_from_db()

        with patch(
            "estacionamientos.models.timezone.now",
            return_value=momento_fin,
        ):
            estacionamiento.finalizar()

        estacionamiento.refresh_from_db()

        self.assertEqual(
            estacionamiento.estado,
            Estacionamiento.Estado.FINALIZADO,
        )

        self.assertEqual(
            estacionamiento.tiempo_utilizado,
            3600,
        )

        self.assertEqual(
            estacionamiento.monto_final,
            Decimal("5000.00"),
        )