from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from .forms import VehiculoForm
from .models import Vehiculo


def verificar_conductor(usuario):
    if not usuario.es_conductor:
        raise PermissionDenied(
            "Solo los conductores pueden administrar vehículos."
        )


@login_required
def mis_vehiculos(request):
    verificar_conductor(request.user)

    vehiculos = Vehiculo.objects.filter(
        propietario=request.user,
    ).order_by(
        "-activo",
        "chapa",
    )

    return render(
        request,
        "vehiculos/mis_vehiculos.html",
        {
            "vehiculos": vehiculos,
        },
    )


@login_required
def registrar_vehiculo(request):
    verificar_conductor(request.user)

    if request.method == "POST":
        form = VehiculoForm(
            request.POST,
            propietario=request.user,
        )

        if form.is_valid():
            vehiculo = form.save()

            messages.success(
                request,
                (
                    f"El vehículo {vehiculo.chapa} "
                    "fue registrado correctamente."
                ),
            )

            return redirect(
                "vehiculos:mis_vehiculos"
            )

    else:
        form = VehiculoForm(
            propietario=request.user,
        )

    return render(
        request,
        "vehiculos/registrar.html",
        {
            "form": form,
        },
    )