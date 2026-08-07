from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from .forms import RegistroConductorForm


def redirigir_segun_rol(usuario):
    if usuario.is_superuser or usuario.es_administrador:
        return redirect("admin:index")

    if usuario.es_inspector:
        return redirect(
            "estacionamientos:verificar_chapa"
        )

    if usuario.es_conductor:
        return redirect(
            "estacionamientos:activos"
        )

    return redirect("usuarios:login")

def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirigir_segun_rol(request.user)

    if request.method == "POST":
        form = AuthenticationForm(
            request=request,
            data=request.POST,
        )

        if form.is_valid():
            usuario = form.get_user()
            auth_login(request, usuario)

            return redirigir_segun_rol(usuario)

    else:
        form = AuthenticationForm(
            request=request,
        )

    return render(
        request,
        "usuarios/login.html",
        {
            "form": form,
        },
    )

def registrar_conductor(request):
    if request.user.is_authenticated:
        return redirigir_segun_rol(request.user)

    if request.method == "POST":
        form = RegistroConductorForm(
            request.POST
        )

        if form.is_valid():
            usuario = form.save()

            auth_login(
                request,
                usuario,
                backend=(
                    "django.contrib.auth.backends."
                    "ModelBackend"
                ),
            )

            messages.success(
                request,
                (
                    "Tu cuenta fue creada correctamente. "
                    "Bienvenido a LuquePark."
                ),
            )

            return redirect(
                "estacionamientos:activos"
            )

    else:
        form = RegistroConductorForm()

    return render(
        request,
        "usuarios/registro.html",
        {
            "form": form,
        },
    )

@require_POST
def cerrar_sesion(request):
    auth_logout(request)

    messages.success(
        request,
        "La sesión se cerró correctamente.",
    )

    return redirect("usuarios:login")

def service_worker(request):
    response = render(
        request,
        "pwa/service-worker.js",
        content_type="application/javascript",
    )

    response["Service-Worker-Allowed"] = "/"
    response["Cache-Control"] = "no-cache"

    return response