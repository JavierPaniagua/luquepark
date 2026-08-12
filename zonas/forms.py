from django import forms

from .models import Zona


class ZonaAdminForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = "__all__"

        widgets = {
            "color_mapa": forms.TextInput(
                attrs={
                    "type": "color",
                }
            ),
            "geometria": forms.HiddenInput(),
        }