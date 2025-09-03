from rest_framework import viewsets, permissions
from .models import ClusterProposal, FinalCluster, DefiningForce
from .serializers import ClusterProposalSerializer, FinalClusterSerializer, DefiningForceSerializer

class ClusterProposalViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Participants to create and manage their own Cluster Proposals.
    """
    serializer_class = ClusterProposalSerializer
    permission_classes = [permissions.IsAuthenticated] # Will need custom permission later

    def get_queryset(self):
        # Users should only see their own proposals
        return ClusterProposal.objects.filter(proposer=self.request.user)

class FinalClusterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for DBAdmins to manage Final Clusters during a meeting.
    """
    queryset = FinalCluster.objects.all()
    serializer_class = FinalClusterSerializer
    permission_classes = [permissions.IsAdminUser] # Only admins can manage final clusters

class DefiningForceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for DBAdmins to manage Defining Forces during a meeting.
    """
    queryset = DefiningForce.objects.all()
    serializer_class = DefiningForceSerializer
    permission_classes = [permissions.IsAdminUser]
