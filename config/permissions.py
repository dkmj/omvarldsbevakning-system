"""Anpassade behörighetsklasser för Django Rest Framework.

Denna modul innehåller anpassade behörighetsklasser som utökar DRFs
standardbeteende för att möta specifika krav i applikationen.
"""

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedByToken(IsAuthenticated):
    """Tillåter endast åtkomst för användare autentiserade via Token.

    Denna behörighetsklass säkerställer att förfrågan är autentiserad
    och att autentiseringen skedde via `TokenAuthentication`. Detta är användbart
    för API-vyer som endast ska vara tillgängliga via token-baserad
    autentisering och inte sessionsbaserad.
    """

    def has_permission(self, request, view):
        """Kontrollerar om användaren är autentiserad via token.

        Returns:
            bool: True om användaren är autentiserad och det skedde via token.
        """
        is_authenticated_by_token = isinstance(
            request.successful_authenticator, TokenAuthentication
        )
        return super().has_permission(request, view) and is_authenticated_by_token
