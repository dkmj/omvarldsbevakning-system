from rest_framework import serializers
from .models import Observation
from accounts.serializers import UserSerializer


class ObservationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and listing a user's own observations.
    """

    # Show author details on read, but it's set automatically on write.
    author = UserSerializer(read_only=True)

    class Meta:
        model = Observation
        fields = [
            "id",
            "period",  # Users must specify which period they are submitting to.
            "title",
            "interest_reason",
            "implications",
            "type",
            "source_link",
            "source_file",
            "tags",
            "author",
            "created_at",
            "status",
        ]
        # These fields are set by the system, not the user.
        read_only_fields = ["author", "created_at", "status"]

    def create(self, validated_data):
        # Automatically set the author to the currently logged-in user.
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
