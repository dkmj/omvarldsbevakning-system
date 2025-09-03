# observations/serializers.py

from rest_framework import serializers

from accounts.models import CustomUser
from clustering.models import Cluster
from clustering.serializers import ClusterSerializer  # Add this import

from .models import Observation


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "role"]


class ObservationSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Observation
        fields = [
            "id",
            "created_at",
            "author",
            "title",
            "source_link",
            "source_file",
            "interest_reason",
            "tags",
            "status",
            "clusters",
        ]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class AdminObservationSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    # Add this line to show full cluster details, not just IDs
    clusters = ClusterSerializer(many=True, read_only=True)

    class Meta:
        model = Observation
        fields = [
            "id",
            "created_at",
            "author",
            "title",
            "source_link",
            "source_file",
            "interest_reason",
            "tags",
            "status",
            "clusters",  # Add 'clusters' to the fields list
        ]


class AdminObservationDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    clusters = serializers.PrimaryKeyRelatedField(
        queryset=Cluster.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Observation
        read_only_fields = [
            "id",
            "created_at",
            "author",
            "title",
            "source_link",
            "source_file",
            "interest_reason",
            "tags",
        ]
        fields = read_only_fields + ["status", "clusters"]
