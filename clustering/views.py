"""API views for the clustering app."""

from rest_framework import viewsets, permissions
from .models import ClusterProposal, FinalCluster, DefiningForce
from .serializers import (
    ClusterProposalSerializer,
    FinalClusterSerializer,
    DefiningForceSerializer,
)


class ClusterProposalViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users to create and manage their own Cluster Proposals.

    Provides full CRUD functionality for ClusterProposal instances. Users are
    restricted to only see and manage their own proposals.
    """

    serializer_class = ClusterProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filters the queryset to return only proposals for the current user.

        This method ensures that users can only view and interact with their
        own `ClusterProposal` objects, providing object-level permissions.

        Returns:
            QuerySet: A queryset of `ClusterProposal` objects filtered by the
        for the currently authenticated user.
        """
        return ClusterProposal.objects.filter(proposer=self.request.user)


class FinalClusterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for admins to manage Final Clusters.

    Provides full CRUD functionality for FinalCluster instances. Access is
    restricted to admin users.
    """

    queryset = FinalCluster.objects.all()
    serializer_class = FinalClusterSerializer
    permission_classes = [permissions.IsAdminUser]


class DefiningForceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for admins to manage Defining Forces.

    Provides full CRUD functionality for DefiningForce instances. Access is
    restricted to admin users.
    """

    queryset = DefiningForce.objects.all()
    serializer_class = DefiningForceSerializer
    permission_classes = [permissions.IsAdminUser]
