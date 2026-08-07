import re

from django import forms

from vehiculos.models import Vehiculo
from zonas.models import Zona

from .models import Estacionamiento


class IniciarEstacionamientoForm(forms.ModelForm):
    class Meta:
        model = Estacionamiento
        fields = (
            "vehiculo",
            "zona",
        )

        labels = {
            "vehiculo": "Seleccione su vehículo",
            "zona": "Seleccione la zona",
        }

        widgets = {
            "vehiculo": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "zona": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def __init__(self, *args, conductor=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.conductor = conductor

        # Por seguridad, inicialmente no mostramos ningún vehículo.
        self.fields["vehiculo"].queryset = Vehiculo.objects.none()

        if conductor is not None:
            # Asignamos el conductor antes de validar el modelo.
            self.instance.conductor = conductor

            # Solo se muestran vehículos activos del conductor
            # que no tengan un estacionamiento activo.
            self.fields["vehiculo"].queryset = (
                Vehiculo.objects.filter(
                    propietario=conductor,
                    activo=True,
                )
                .exclude(
                    estacionamientos__estado=Estacionamiento.Estado.ACTIVO,
                )
                .order_by("chapa")
            )

        # Solo se pueden seleccionar zonas activas.
        self.fields["zona"].queryset = Zona.objects.filter(
            activa=True,
        ).order_by("nombre")

    def save(self, commit=True):
        estacionamiento = super().save(commit=False)
        estacionamiento.conductor = self.conductor

        if commit:
            estacionamiento.save()

        return estacionamiento

class VerificarChapaForm(forms.Form):
    chapa = forms.CharField(
        label="Número de chapa",
        max_length=15,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg text-uppercase",
                "placeholder": "Ejemplo: ABCD123",
                "autocomplete": "off",
                "autofocus": True,
            }
        ),
    )

    def clean_chapa(self):
        chapa = self.cleaned_data["chapa"]

        # Convierte: abcd 123 o abcd-123 en ABCD123.
        chapa_normalizada = re.sub(
            r"[^A-Za-z0-9]",
            "",
            chapa,
        ).upper()

        if len(chapa_normalizada) < 3:
            raise forms.ValidationError(
                "Ingrese un número de chapa válido."
            )

        return chapa_normalizada