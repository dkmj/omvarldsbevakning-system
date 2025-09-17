# scan_periods/serializers.py

from rest_framework import serializers
from .models import Period


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "status",
            "participants",
            "db_admins",
        ]
