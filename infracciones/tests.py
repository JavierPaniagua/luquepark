from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from vehiculos.models import Vehiculo

from .models import Infraccion


Usuario = get_user_model()


class MisInfraccionesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.conductor_uno = Usuario.objects.create_user(
            username="conductor1",
            password="Prueba12345",
            first_name="Juan",
            last_name="Pérez",
            rol="CONDUCTOR",
        )

        cls.conductor_dos = Usuario.objects.create_user(
            username="conductor2",
            password="Prueba12345",
            first_name="Pedro",
            last_name="López",
            rol="CONDUCTOR",
        )

        cls.inspector = Usuario.objects.create_user(
            username="inspector1",
            password="Prueba12345",
            first_name="Carlos",
            last_name="Benítez",
            rol="INSPECTOR",
        )

        # Obtiene automáticamente el primer valor válido
        # de las opciones del campo tipo.
        tipo_vehiculo = (
            Vehiculo._meta
            .get_field("tipo")
            .choices[0][0]
        )

        cls.vehiculo_uno = Vehiculo.objects.create(
            propietario=cls.conductor_uno,
            chapa="ABC123",
            tipo=tipo_vehiculo,
            marca="Toyota",
            modelo="Premio",
            color="Negro",
        )

        cls.vehiculo_dos = Vehiculo.objects.create(
            propietario=cls.conductor_dos,
            chapa="XYZ987",
            tipo=tipo_vehiculo,
            marca="Kia",
            modelo="Picanto",
            color="Blanco",
        )

        cls.infraccion_uno = Infraccion.objects.create(
            inspector=cls.inspector,
            vehiculo=cls.vehiculo_uno,
            chapa=cls.vehiculo_uno.chapa,
            motivo=Infraccion.Motivo.SIN_ESTACIONAMIENTO,
            observaciones="Vehículo sin estacionamiento activo.",
        )

        cls.infraccion_dos = Infraccion.objects.create(
            inspector=cls.inspector,
            vehiculo=cls.vehiculo_dos,
            chapa=cls.vehiculo_dos.chapa,
            motivo=Infraccion.Motivo.ZONA_INCORRECTA,
            observaciones="Vehículo estacionado en otra zona.",
        )

        cls.url = reverse(
            "infracciones:mis_infracciones"
        )

    def test_conductor_ve_su_propia_infraccion(self):
        self.client.force_login(
            self.conductor_uno
        )

        respuesta = self.client.get(
            self.url
        )

        self.assertEqual(
            respuesta.status_code,
            200,
        )

        self.assertContains(
            respuesta,
            self.vehiculo_uno.chapa,
        )

        self.assertContains(
            respuesta,
            "Sin estacionamiento activo",
        )

    def test_conductor_no_ve_infracciones_ajenas(self):
        self.client.force_login(
            self.conductor_uno
        )

        respuesta = self.client.get(
            self.url
        )

        self.assertEqual(
            respuesta.status_code,
            200,
        )

        self.assertContains(
            respuesta,
            self.vehiculo_uno.chapa,
        )

        self.assertNotContains(
            respuesta,
            self.vehiculo_dos.chapa,
        )

        self.assertNotContains(
            respuesta,
            "Vehículo estacionado en otra zona.",
        )

    def test_inspector_no_puede_entrar_a_mis_infracciones(self):
        self.client.force_login(
            self.inspector
        )

        respuesta = self.client.get(
            self.url
        )

        self.assertEqual(
            respuesta.status_code,
            403,
        )