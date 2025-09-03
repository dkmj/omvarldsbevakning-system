# observations/views.py

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.parsers import FormParser, MultiPartParser

from .filters import ObservationFilter
from .models import Observation
from .serializers import (
    AdminObservationDetailSerializer,
    AdminObservationSerializer,
    ObservationSerializer,
)


class ObservationListCreateView(generics.ListCreateAPIView):
    serializer_class = ObservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Observation.objects.filter(author=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


class AdminObservationListView(generics.ListAPIView):
    queryset = Observation.objects.all().order_by("-created_at")
    serializer_class = AdminObservationSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ObservationFilter


class AdminObservationDetailView(generics.RetrieveUpdateAPIView):
    queryset = Observation.objects.all()
    serializer_class = AdminObservationDetailSerializer
    permission_classes = [permissions.IsAdminUser]
