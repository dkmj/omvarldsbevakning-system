"""API-vyer för appen `accounts`."""

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """API-endpoint för registrering av nya användare.

    Denna vy tillåter alla användare (autentiserade eller ej) att skapa ett
    nytt användarkonto. Använder `RegisterSerializer` för att hantera logiken.
    """

    queryset = UserSerializer.Meta.model.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class UserDetailView(APIView):
    """API-endpoint för att hämta detaljer om den inloggade användaren.

    Kräver att användaren är autentiserad. Vid en GET-förfrågan serialiseras
    och returneras `request.user`-objektet.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Hanterar GET-förfrågningar för att returnera användardetaljer.

        Args:
            request: Request-objektet som innehåller den autentiserade användaren.

        Returns:
            Response: Ett Response-objekt med serialiserad användardata.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
