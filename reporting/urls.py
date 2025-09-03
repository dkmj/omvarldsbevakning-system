# reporting/urls.py

from django.urls import path

from .views import ReportView

urlpatterns = [
    path("report/", ReportView.as_view(), name="observation-report"),
]
