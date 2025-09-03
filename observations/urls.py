from django.urls import path
from .views import ObservationListCreateView

urlpatterns = [
    # This is now the only URL pattern in this file.
    path('', ObservationListCreateView.as_view(), name='observation-list-create'),
]
