from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Zona


@login_required
def mapa_zonas(request):
    zonas_consulta = Zona.objects.filter(
        activa=True,
        latitud__isnull=False,
        longitud__isnull=False,
    ).order_by("nombre")

    zonas = [
        {
            "id": zona.id,
            "nombre": zona.nombre,
            "codigo": zona.codigo,
            "descripcion": zona.descripcion,
            "tarifa_hora": str(zona.tarifa_hora),
            "hora_inicio": zona.hora_inicio.strftime("%H:%M"),
            "hora_fin": zona.hora_fin.strftime("%H:%M"),
            "latitud": float(zona.latitud),
            "longitud": float(zona.longitud),
        }
        for zona in zonas_consulta
    ]

    return render(
        request,
        "zonas/mapa.html",
        {
            "zonas": zonas,
        },
    )