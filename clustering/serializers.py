"""Serializers for the clustering app."""

from rest_framework import serializers
from .models import ClusterProposal, FinalCluster, DefiningForce
from observations.serializers import ObservationSerializer


class ClusterProposalSerializer(serializers.ModelSerializer):
    """Serializer for the ClusterProposal model."""

    class Meta:
        model = ClusterProposal
        fields = "__all__"


class FinalClusterSerializer(serializers.ModelSerializer):
    """Serializer for the FinalCluster model.

    Includes nested serialization for related observations to provide
    detailed information in the API response.
    """

    # We can show full observation details within the final cluster
    observations = ObservationSerializer(many=True, read_only=True)

    class Meta:
        model = FinalCluster
        fields = "__all__"


class DefiningForceSerializer(serializers.ModelSerializer):
    """Serializer for the DefiningForce model."""

    class Meta:
        model = DefiningForce
        fields = "__all__"
