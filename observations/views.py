from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Observation
from .serializers import ObservationSerializer


class ObservationListCreateView(generics.ListCreateAPIView):
    """
    Allows contributors to list their own observations and create new ones.
    """

    serializer_class = ObservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # This ensures users can only see their own observations.
        # We will need to update this later to filter by the active period.
        return Observation.objects.filter(author=self.request.user).order_by(
            "-created_at"
        )

    def get_serializer_context(self):
        # Pass the request context to the serializer.
        return {"request": self.request}


# NOTE: The old admin views (AdminObservationListView, AdminObservationDetailView)
# have been removed. Their functionality will be rebuilt in the other apps
# to match our new, more detailed process.
