# observations/models.py

from django.conf import settings
from django.db import models

from clustering.models import Cluster  # Add this import


class Observation(models.Model):
    # New: Moderation Status Field
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        UNCERTAIN = "UNCERTAIN", "Uncertain"
        DELETION = "DELETION", "Deletion"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    clusters = models.ManyToManyField(Cluster, blank=True, related_name="observations")

    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="observations",
    )

    title = models.CharField(max_length=255)

    source_link = models.URLField(max_length=500, blank=True, null=True)

    # This is the new field for file uploads
    source_file = models.FileField(
        upload_to="observations/%Y/%m/%d/", blank=True, null=True
    )

    interest_reason = models.TextField(max_length=500)

    tags = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'"{self.title}" by {self.author.username}'
