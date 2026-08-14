import re

from django.core.paginator import Paginator
from .models import Infraccion
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from estacionamientos.models import Estacionamiento
from vehiculos.models import Vehiculo

from .forms import RegistrarInfraccionForm


def verificar_inspector(usuario):
    if not usuario.es_inspector:
        raise PermissionDenied(
            "Solo los inspectores pueden registrar infracciones."
        )


@login_required
def registrar_infraccion(request, chapa):
    verificar_inspector(request.user)

    chapa_normalizada = re.sub(
        r"[^A-Za-z0-9]",
        "",
        chapa,
    ).upper()

    vehiculo = Vehiculo.objects.filter(
        chapa=chapa_normalizada,
    ).first()

    tiene_estacionamiento_activo = (
        Estacionamiento.objects.filter(
            vehiculo__chapa=chapa_normalizada,
            estado=Estacionamiento.Estado.ACTIVO,
        ).exists()
    )

    if tiene_estacionamiento_activo:
        messages.error(
            request,
            (
                "No se puede registrar la infracción porque "
                "el vehículo tiene un estacionamiento activo."
            ),
        )

        return redirect(
            "estacionamientos:verificar_chapa"
        )

    if request.method == "POST":
        form = RegistrarInfraccionForm(
            request.POST,
            inspector=request.user,
            chapa=chapa_normalizada,
            vehiculo=vehiculo,
        )

        if form.is_valid():
            infraccion = form.save()

            messages.success(
                request,
                (
                    f"Infracción registrada correctamente "
                    f"para la chapa {infraccion.chapa}."
                ),
            )

            return redirect(
                "estacionamientos:verificar_chapa"
            )

    else:
        form = RegistrarInfraccionForm(
            inspector=request.user,
            chapa=chapa_normalizada,
            vehiculo=vehiculo,
        )

    return render(
        request,
        "infracciones/registrar.html",
        {
            "form": form,
            "chapa": chapa_normalizada,
            "vehiculo": vehiculo,
        },
    )

@login_required
def mis_infracciones(request):
    if not request.user.es_conductor:
        raise PermissionDenied(
            "Solo los conductores pueden consultar sus infracciones."
        )

    infracciones = (
        Infraccion.objects
        .filter(vehiculo__propietario=request.user)
        .select_related("vehiculo", "zona", "inspector")
        .order_by("-fecha_registro")
    )

    paginador = Paginator(infracciones, 10)
    pagina = paginador.get_page(request.GET.get("pagina"))

    return render(
        request,
        "infracciones/mis_infracciones.html",
        {
            "pagina": pagina,
        },
    )