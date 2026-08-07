from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class RegistroConductorForm(UserCreationForm):
    class Meta:
        model = Usuario

        fields = (
            "username",
            "first_name",
            "last_name",
            "cedula",
            "telefono",
            "password1",
            "password2",
        )

        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "cedula": "Número de cédula",
            "telefono": "Teléfono",
            "password1": "Contraseña",
            "password2": "Confirmar contraseña",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-control"

        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "Ejemplo: pedro123",
                "autocomplete": "username",
            }
        )

        self.fields["first_name"].widget.attrs["placeholder"] = (
            "Ingrese sus nombres"
        )

        self.fields["last_name"].widget.attrs["placeholder"] = (
            "Ingrese sus apellidos"
        )

        self.fields["cedula"].widget.attrs["placeholder"] = (
            "Ingrese su número de cédula"
        )

        self.fields["telefono"].widget.attrs["placeholder"] = (
            "Ejemplo: 0981123456"
        )

    def save(self, commit=True):
        usuario = super().save(commit=False)

        # El registro público siempre crea conductores.
        usuario.rol = "CONDUCTOR"

        if commit:
            usuario.save()

        return usuario