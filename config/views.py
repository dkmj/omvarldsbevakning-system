"""Vyer för projektets kärnfunktionalitet (config)."""

from django.shortcuts import render


def login_view(request):
    """Renderar inloggningssidan.

    Args:
        request: HttpRequest-objektet.

    Returns:
        HttpResponse: Renderad HTML för inloggningssidan.
    """
    return render(request, "login.html")


def dashboard_view(request):
    """Renderar huvudsidan (dashboard).

    Args:
        request: HttpRequest-objektet.

    Returns:
        HttpResponse: Renderad HTML för huvudsidan.
    """
    return render(request, "dashboard.html")
