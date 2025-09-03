from django.db import models
from django.conf import settings


class Period(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        CLUSTERING = "CLUSTERING", "Clustering"
        MEETING = "MEETING", "Meeting"
        ARCHIVED = "ARCHIVED", "Archived"

    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.OPEN
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="participating_periods", blank=True
    )
    db_admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="admin_periods", blank=True
    )

    def __str__(self):
        return self.name
