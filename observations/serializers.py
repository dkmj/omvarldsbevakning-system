from rest_framework import serializers
from .models import Observation
from accounts.serializers import UserSerializer # We keep this for author details

class ObservationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and listing a user's own observations.
    """
    # Make the author field read-only as it's set automatically.
    author = UserSerializer(read_only=True)

    class Meta:
        model = Observation
        fields = [
            'id',
            'period', # Observations must now be submitted to a period
            'title',
            'interest_reason',
            'implications',
            'type',
            'source_link',
            'source_file',
            'tags',
            'author',
            'created_at',
            'status',
        ]
        # The 'period' is writeable, but some fields are read-only
        read_only_fields = ['author', 'created_at', 'status']

    def create(self, validated_data):
        # Set the author from the request context.
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

# NOTE: The old AdminObservationSerializer and AdminObservationDetailSerializer
# have been removed from this file. Their functionality will be rebuilt in the
# other apps (scan_periods and clustering) to match our new, more detailed process.
