# core/urls.py

from django.urls import path

from .views import dashboard_view, login_view

urlpatterns = [
    path("", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
]
