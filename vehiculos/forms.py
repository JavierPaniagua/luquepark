from django import forms

from .models import Vehiculo


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo

        fields = (
            "chapa",
            "tipo",
            "marca",
            "modelo",
            "color",
        )

        labels = {
            "chapa": "Número de chapa",
            "tipo": "Tipo de vehículo",
            "marca": "Marca",
            "modelo": "Modelo",
            "color": "Color",
        }

        widgets = {
            "chapa": forms.TextInput(
                attrs={
                    "class": "form-control text-uppercase",
                    "placeholder": "Ejemplo: ABCD123",
                    "autocomplete": "off",
                }
            ),
            "tipo": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "marca": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: Toyota",
                }
            ),
            "modelo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: Premio",
                }
            ),
            "color": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: Blanco",
                }
            ),
        }

    def __init__(self, *args, propietario=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.propietario = propietario

        if propietario is not None:
            self.instance.propietario = propietario

    def save(self, commit=True):
        vehiculo = super().save(commit=False)
        vehiculo.propietario = self.propietario
        vehiculo.activo = True

        if commit:
            vehiculo.save()

        return vehiculo