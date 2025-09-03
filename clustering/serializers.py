from rest_framework import serializers
from .models import ClusterProposal, FinalCluster, DefiningForce
from observations.serializers import ObservationSerializer


class ClusterProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClusterProposal
        fields = "__all__"


class FinalClusterSerializer(serializers.ModelSerializer):
    # We can show full observation details within the final cluster
    observations = ObservationSerializer(many=True, read_only=True)

    class Meta:
        model = FinalCluster
        fields = "__all__"


class DefiningForceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefiningForce
        fields = "__all__"
