from rest_framework import generics, permissions, serializers
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Observation
from accounts.serializers import UserSerializer
from scan_periods.permissions import IsPeriodParticipant
from .serializers import ObservationSerializer  # Correctly import the serializer


class ParticipantObservationSerializer(serializers.ModelSerializer):
    """
    A detailed serializer for the participant view, showing full author info.
    """

    author = UserSerializer(read_only=True)

    class Meta:
        model = Observation
        fields = "__all__"


class ParticipantObservationListView(generics.ListAPIView):
    """
    API endpoint for Participants to view all approved observations for a given period.
    """

    serializer_class = ParticipantObservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsPeriodParticipant]

    def get_queryset(self):
        period_id = self.request.query_params.get("period_id")
        if period_id:
            return Observation.objects.filter(period_id=period_id, status="APPROVED")
        return Observation.objects.none()


class ObservationListCreateView(generics.ListCreateAPIView):
    """
    Allows contributors to list their own observations and create new ones.
    """

    serializer_class = ObservationSerializer  # This will now work correctly
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Observation.objects.filter(author=self.request.user).order_by(
            "-created_at"
        )

    def get_serializer_context(self):
        return {"request": self.request}
