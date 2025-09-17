from django.urls import path
from .views import ObservationListCreateView, ParticipantObservationListView

urlpatterns = [
    # URL for contributors to submit and see their own observations
    path("", ObservationListCreateView.as_view(), name="observation-list-create"),
    # New URL for participants to see all observations for a period,
    # e.g., /api/observations/participant/?period_id=1
    path(
        "participant/",
        ParticipantObservationListView.as_view(),
        name="observation-participant-list",
    ),
]
