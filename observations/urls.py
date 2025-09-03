# observations/urls.py

from django.urls import path

from .views import (
    AdminObservationDetailView,
    AdminObservationListView,
    ObservationListCreateView,
)

urlpatterns = [
    # For contributors to list their own and create new observations
    path("", ObservationListCreateView.as_view(), name="observation-list-create"),
    # For admins to list ALL observations
    path("admin/", AdminObservationListView.as_view(), name="observation-admin-list"),
    # For admins to retrieve and update a SINGLE observation
    path(
        "admin/<int:pk>/",
        AdminObservationDetailView.as_view(),
        name="observation-admin-detail",
    ),
]
