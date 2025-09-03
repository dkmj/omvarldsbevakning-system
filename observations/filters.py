# observations/filters.py

from django_filters import rest_framework as filters

from .models import Observation


class ObservationFilter(filters.FilterSet):
    # Allow searching for text within the title (case-insensitive)
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")

    # Allow searching for text within the reason (case-insensitive)
    interest_reason = filters.CharFilter(
        field_name="interest_reason", lookup_expr="icontains"
    )

    # Allow searching for text within the tags (case-insensitive)
    tags = filters.CharFilter(field_name="tags", lookup_expr="icontains")

    class Meta:
        model = Observation
        # Define all fields that can be filtered on
        fields = ["title", "interest_reason", "tags", "status"]
