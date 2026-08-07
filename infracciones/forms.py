from django import forms

from zonas.models import Zona

from .models import Infraccion


class RegistrarInfraccionForm(forms.ModelForm):
    class Meta:
        model = Infraccion

        fields = (
            "zona",
            "motivo",
            "observaciones",
        )

        labels = {
            "zona": "Zona",
            "motivo": "Motivo de la infracción",
            "observaciones": "Observaciones",
        }

        widgets = {
            "zona": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "motivo": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": (
                        "Información adicional de la infracción"
                    ),
                }
            ),
        }

    def __init__(
        self,
        *args,
        inspector=None,
        chapa=None,
        vehiculo=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.inspector = inspector
        self.chapa = chapa
        self.vehiculo = vehiculo

        self.instance.inspector = inspector
        self.instance.chapa = chapa
        self.instance.vehiculo = vehiculo

        self.fields["zona"].queryset = Zona.objects.filter(
            activa=True,
        ).order_by("nombre")

    def save(self, commit=True):
        infraccion = super().save(commit=False)

        infraccion.inspector = self.inspector
        infraccion.chapa = self.chapa
        infraccion.vehiculo = self.vehiculo

        if commit:
            infraccion.save()

        return infraccion