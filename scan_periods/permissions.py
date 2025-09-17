from rest_framework import permissions
from .models import Period


class IsPeriodParticipant(permissions.BasePermission):
    """
    Custom permission to only allow users who are participants of a period.
    """

    def has_permission(self, request, view):
        # We expect the period ID to be in the URL's query parameters
        period_id = request.query_params.get("period_id")
        if not period_id:
            return False  # Deny access if no period is specified

        try:
            period = Period.objects.get(pk=period_id)
            # Check if the requesting user is in the participants list for this period
            return request.user in period.participants.all()
        except Period.DoesNotExist:
            return False
