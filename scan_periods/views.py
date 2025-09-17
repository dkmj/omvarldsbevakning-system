# scan_periods/views.py

from rest_framework import viewsets, permissions
from .models import Period
from .serializers import PeriodSerializer


class PeriodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows periods to be viewed.
    Access is restricted to authenticated users.
    """

    queryset = Period.objects.all().order_by("-start_date")
    serializer_class = PeriodSerializer
    permission_classes = [permissions.IsAuthenticated]
