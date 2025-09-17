# scan_periods/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"periods", views.PeriodViewSet, basename="period")

urlpatterns = [
    path("", include(router.urls)),
]
