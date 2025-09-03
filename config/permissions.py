# config/permissions.py

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedByToken(IsAuthenticated):
    """
    Custom permission to only allow access to users authenticated via Token.
    This bypasses CSRF checks for our API views.
    """

    def has_permission(self, request, view):
        is_authenticated_by_token = isinstance(
            request.successful_authenticator, TokenAuthentication
        )
        return super().has_permission(request, view) and is_authenticated_by_token
