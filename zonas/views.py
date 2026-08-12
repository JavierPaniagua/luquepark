from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .models import Zona


@login_required
def mapa_zonas(request):
    zonas_consulta = (
        Zona.objects.filter(
            activa=True,
        )
        .filter(
            Q(
                latitud__isnull=False,
                longitud__isnull=False,
            )
            | Q(
                geometria__isnull=False,
            )
        )
        .order_by("nombre")
    )

    zonas = []

    for zona in zonas_consulta:
        zonas.append(
            {
                "id": zona.id,
                "nombre": zona.nombre,
                "codigo": zona.codigo,
                "descripcion": zona.descripcion,
                "tarifa_hora": str(zona.tarifa_hora),
                "hora_inicio": zona.hora_inicio.strftime(
                    "%H:%M"
                ),
                "hora_fin": zona.hora_fin.strftime(
                    "%H:%M"
                ),
                "latitud": (
                    float(zona.latitud)
                    if zona.latitud is not None
                    else None
                ),
                "longitud": (
                    float(zona.longitud)
                    if zona.longitud is not None
                    else None
                ),
                "color_mapa": (
                    zona.color_mapa or "#20c997"
                ),
                "geometria": zona.geometria,
            }
        )

    return render(
        request,
        "zonas/mapa.html",
        {
            "zonas": zonas,
        },
    )