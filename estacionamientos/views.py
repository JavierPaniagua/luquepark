from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from vehiculos.models import Vehiculo

from .forms import (
    IniciarEstacionamientoForm,
    VerificarChapaForm,
)
from .models import Estacionamiento


def verificar_conductor(usuario):
    if not usuario.es_conductor:
        raise PermissionDenied(
            "Solo los conductores pueden realizar esta operación."
        )


def verificar_inspector(usuario):
    if not usuario.es_inspector:
        raise PermissionDenied(
            "Solo los inspectores pueden verificar chapas."
        )


def verificar_administrador(usuario):
    if not (
        usuario.is_superuser
        or usuario.es_administrador
    ):
        raise PermissionDenied(
            "Solo los administradores pueden consultar reportes."
        )


@login_required
def panel_conductor(request):
    verificar_conductor(request.user)

    estacionamientos_activos = (
        Estacionamiento.objects.filter(
            conductor=request.user,
            estado=Estacionamiento.Estado.ACTIVO,
        )
        .select_related(
            "vehiculo",
            "zona",
        )
        .order_by("-fecha_inicio")
    )

    zona_id = request.GET.get("zona")
    datos_iniciales = {}

    if zona_id:
        datos_iniciales["zona"] = zona_id

    form = IniciarEstacionamientoForm(
        conductor=request.user,
        initial=datos_iniciales,
    )

    contexto = {
        "form": form,
        "estacionamientos_activos": (
            estacionamientos_activos
        ),
        "cantidad_vehiculos": (
            request.user.vehiculos.filter(
                activo=True,
            ).count()
        ),
    }

    return render(
        request,
        "estacionamientos/panel_conductor.html",
        contexto,
    )


@login_required
def iniciar_estacionamiento(request):
    verificar_conductor(request.user)

    if request.method == "POST":
        form = IniciarEstacionamientoForm(
            request.POST,
            conductor=request.user,
        )

        if form.is_valid():
            try:
                with transaction.atomic():
                    estacionamiento = form.save()

                messages.success(
                    request,
                    (
                        "Estacionamiento iniciado correctamente para "
                        f"{estacionamiento.vehiculo.chapa}."
                    ),
                )

                return redirect(
                    "estacionamientos:activos"
                )

            except (IntegrityError, ValidationError):
                form.add_error(
                    "vehiculo",
                    (
                        "No se pudo iniciar el estacionamiento. "
                        "El vehículo podría tener otro "
                        "estacionamiento activo."
                    ),
                )

    else:
        zona_id = request.GET.get("zona")

        datos_iniciales = {}

        if zona_id:
            datos_iniciales["zona"] = zona_id

        form = IniciarEstacionamientoForm(
            conductor=request.user,
            initial=datos_iniciales,
        )

    return render(
        request,
        "estacionamientos/iniciar.html",
        {
            "form": form,
        },
    )


@login_required
def estacionamientos_activos(request):
    verificar_conductor(request.user)

    estacionamientos = (
        Estacionamiento.objects.filter(
            conductor=request.user,
            estado=Estacionamiento.Estado.ACTIVO,
        )
        .select_related(
            "vehiculo",
            "zona",
        )
        .order_by("-fecha_inicio")
    )

    return render(
        request,
        "estacionamientos/activos.html",
        {
            "estacionamientos": estacionamientos,
        },
    )


@login_required
@require_POST
def finalizar_estacionamiento(
    request,
    estacionamiento_id,
):
    verificar_conductor(request.user)

    try:
        with transaction.atomic():
            estacionamiento = get_object_or_404(
                Estacionamiento.objects.select_for_update(),
                id=estacionamiento_id,
                conductor=request.user,
            )

            estacionamiento.finalizar()

        messages.success(
            request,
            (
                f"Estacionamiento de "
                f"{estacionamiento.vehiculo.chapa} "
                f"finalizado. Monto: Gs. "
                f"{estacionamiento.monto_final}."
            ),
        )

    except ValidationError as error:
        messages.error(
            request,
            error.messages[0],
        )

    return redirect(
        "estacionamientos:activos"
    )


@login_required
def verificar_chapa(request):
    verificar_inspector(request.user)

    resultado = None

    if request.method == "POST":
        form = VerificarChapaForm(
            request.POST
        )

        if form.is_valid():
            chapa = form.cleaned_data["chapa"]

            vehiculo = (
                Vehiculo.objects.filter(
                    chapa=chapa,
                    activo=True,
                )
                .select_related("propietario")
                .first()
            )

            if vehiculo is None:
                resultado = {
                    "estado": "NO_REGISTRADO",
                    "chapa": chapa,
                    "mensaje": (
                        "La chapa no se encuentra registrada "
                        "en LuquePark."
                    ),
                }

            else:
                estacionamiento = (
                    Estacionamiento.objects.filter(
                        vehiculo=vehiculo,
                        estado=(
                            Estacionamiento.Estado.ACTIVO
                        ),
                    )
                    .select_related(
                        "vehiculo",
                        "zona",
                        "conductor",
                    )
                    .first()
                )

                if estacionamiento:
                    resultado = {
                        "estado": "ACTIVO",
                        "chapa": chapa,
                        "vehiculo": vehiculo,
                        "estacionamiento": estacionamiento,
                        "monto_aproximado": (
                            estacionamiento.calcular_monto()
                        ),
                    }

                else:
                    resultado = {
                        "estado": "SIN_ESTACIONAMIENTO",
                        "chapa": chapa,
                        "vehiculo": vehiculo,
                        "mensaje": (
                            "El vehículo está registrado, "
                            "pero no tiene un estacionamiento "
                            "activo."
                        ),
                    }

    else:
        form = VerificarChapaForm()

    return render(
        request,
        "estacionamientos/verificar_chapa.html",
        {
            "form": form,
            "resultado": resultado,
        },
    )


@login_required
def historial_estacionamientos(request):
    verificar_conductor(request.user)

    estacionamientos = (
        Estacionamiento.objects.filter(
            conductor=request.user,
            estado=Estacionamiento.Estado.FINALIZADO,
        )
        .select_related(
            "vehiculo",
            "zona",
        )
        .order_by("-fecha_fin")
    )

    paginador = Paginator(
        estacionamientos,
        10,
    )

    pagina = paginador.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "estacionamientos/historial.html",
        {
            "pagina": pagina,
        },
    )


@login_required
def reporte_general(request):
    verificar_administrador(request.user)

    resumen = Estacionamiento.objects.aggregate(
        total=Count("id"),

        activos=Count(
            "id",
            filter=Q(
                estado=Estacionamiento.Estado.ACTIVO
            ),
        ),

        finalizados=Count(
            "id",
            filter=Q(
                estado=Estacionamiento.Estado.FINALIZADO
            ),
        ),

        monto_recaudado=Sum(
            "monto_final",
            filter=Q(
                estado=Estacionamiento.Estado.FINALIZADO
            ),
            default=0,
        ),
    )

    ultimos_estacionamientos = (
        Estacionamiento.objects.filter(
            estado=Estacionamiento.Estado.FINALIZADO,
        )
        .select_related(
            "conductor",
            "vehiculo",
            "zona",
        )
        .order_by("-fecha_fin")[:10]
    )

    return render(
        request,
        "estacionamientos/reporte_general.html",
        {
            "resumen": resumen,
            "ultimos_estacionamientos": (
                ultimos_estacionamientos
            ),
        },
    )