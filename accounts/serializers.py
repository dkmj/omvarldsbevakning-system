# accounts/serializers.py

from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer for displaying user information."""

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "role")


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for creating (registering) a new user."""

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # We override create to handle password hashing.
        user = CustomUser.objects.create_user(
            validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        # The default role 'EXPERT' from the model will be used.
        return user
