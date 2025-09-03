# clustering/views.py

from rest_framework import permissions, viewsets

from .models import Cluster
from .serializers import ClusterSerializer


class ClusterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clusters to be viewed or edited by admins.
    """

    queryset = Cluster.objects.all().order_by("name")
    serializer_class = ClusterSerializer
    permission_classes = [permissions.IsAdminUser]
