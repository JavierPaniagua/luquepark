from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "cedula",
        "telefono",
        "rol",
        "is_active",
    )

    list_filter = (
        "rol",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "cedula",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Datos de LuquePark",
            {
                "fields": (
                    "cedula",
                    "telefono",
                    "rol",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Datos de LuquePark",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "cedula",
                    "telefono",
                    "rol",
                )
            },
        ),
    )