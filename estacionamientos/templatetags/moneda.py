from decimal import Decimal, InvalidOperation

from django import template


register = template.Library()


@register.filter
def numero_py(valor):
    """
    Formatea números como:
    580008.34 -> 580.008,34
    """
    if valor is None or valor == "":
        return "0,00"

    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError):
        return valor

    formato = f"{numero:,.2f}"

    return (
        formato
        .replace(",", "_")
        .replace(".", ",")
        .replace("_", ".")
    )