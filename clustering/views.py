from rest_framework import viewsets, permissions
from .models import ClusterProposal, FinalCluster, DefiningForce
from .serializers import (
    ClusterProposalSerializer,
    FinalClusterSerializer,
    DefiningForceSerializer,
)


class ClusterProposalViewSet(viewsets.ModelViewSet):
    """
    API endpoint for participants to view and edit their own cluster proposals.
    """

    serializer_class = ClusterProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see and edit their own proposals.
        # We also filter by the active period from the URL.
        period_id = self.request.query_params.get("period_id")
        queryset = ClusterProposal.objects.filter(proposer=self.request.user)
        if period_id:
            queryset = queryset.filter(period_id=period_id)
        return queryset

    def get_serializer_context(self):
        # Pass request to the serializer to automatically set the proposer.
        return {"request": self.request}


class FinalClusterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for DBAdmins to view and edit final clusters.
    """

    queryset = FinalCluster.objects.all()
    serializer_class = FinalClusterSerializer
    permission_classes = [
        permissions.IsAdminUser
    ]  # Only admins can manage final clusters


class DefiningForceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for DBAdmins to view and edit defining forces.
    """

    queryset = DefiningForce.objects.all()
    serializer_class = DefiningForceSerializer
    permission_classes = [permissions.IsAdminUser]
