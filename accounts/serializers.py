"""Serializers för appen `accounts`, hanterar användardata."""

from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer för `CustomUser`-modellen.

    Används för läsoperationer för att säkert visa användarinformation,
    exklusive känslig data som lösenord.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "role")


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer för att skapa (registrera) en ny användare.

    Hanterar skapandet av användare och säkerställer att lösenordet är
    write-only och hashas korrekt.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Skapar och returnerar en ny `CustomUser`-instans.

        Denna metod använder Djangos `create_user`-hjälpfunktion för att
        säkerställa att lösenordet hashas korrekt.

        Args:
            validated_data (dict): Validerad data från serializern.

        Returns:
            CustomUser: Den nyskapade användarinstansen.
        """
        user = CustomUser.objects.create_user(
            validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        # The default role 'EXPERT' from the model will be used.
        return user
