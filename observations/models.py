from django.conf import settings
from django.db import models


class Observation(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        UNCERTAIN = "UNCERTAIN", "Uncertain"
        DELETION = "DELETION", "Deletion"

    class ObservationType(models.TextChoices):
        SIGNAL = "SIGNAL", "Signal of Change"
        REFRAMING = "REFRAMING", "Reframing"
        DISCONTINUITY = "DISCONTINUITY", "Discontinuity"
        OUTLIER = "OUTLIER", "Outlier"

    # Use a string reference ('app_name.ModelName') to avoid circular imports
    period = models.ForeignKey(
        "scan_periods.Period", on_delete=models.CASCADE, related_name="observations"
    )
    implications = models.TextField(
        blank=True, help_text="Potentiella konsekvenser av denna observation."
    )
    type = models.CharField(
        max_length=20, choices=ObservationType.choices, default=ObservationType.SIGNAL
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="observations"
    )
    title = models.CharField(max_length=255)
    source_link = models.URLField(max_length=500, blank=True, null=True)
    source_file = models.FileField(
        upload_to="observations/%Y/%m/%d/", blank=True, null=True
    )
    interest_reason = models.TextField(max_length=500)
    tags = models.CharField(max_length=255, blank=True)

    def __str__(self):
        # The self.period relationship will be fully resolved when this method is called
        try:
            return f'"{self.title}" in period "{self.period.name}"'
        except self._meta.model.period.RelatedObjectDoesNotExist:
            return f'"{self.title}" (no period assigned)'
