from rest_framework import serializers
from .models import ClusterProposal, FinalCluster, DefiningForce
from accounts.serializers import UserSerializer


class DefiningForceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefiningForce
        fields = ["id", "period", "name", "description"]


class FinalClusterSerializer(serializers.ModelSerializer):
    # To show full details instead of just IDs
    defining_forces = DefiningForceSerializer(many=True, read_only=True)

    class Meta:
        model = FinalCluster
        fields = [
            "id",
            "period",
            "name",
            "motivation",
            "robustness_score",
            "color",
            "observations",
            "defining_forces",
        ]


class ClusterProposalSerializer(serializers.ModelSerializer):
    # Show the proposer's details, but make it read-only
    proposer = UserSerializer(read_only=True)

    class Meta:
        model = ClusterProposal
        fields = [
            "id",
            "period",
            "proposer",
            "name",
            "motivation",
            "color",
            "observations",
        ]

    def create(self, validated_data):
        # Automatically set the proposer to the current user
        validated_data["proposer"] = self.context["request"].user
        return super().create(validated_data)
