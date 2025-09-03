from django.db import models
from django.conf import settings


class DefiningForce(models.Model):
    # Use a string reference ('app_name.ModelName') to avoid circular imports
    period = models.ForeignKey(
        "scan_periods.Period", on_delete=models.CASCADE, related_name="defining_forces"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class FinalCluster(models.Model):
    period = models.ForeignKey(
        "scan_periods.Period", on_delete=models.CASCADE, related_name="final_clusters"
    )
    name = models.CharField(max_length=100)
    motivation = models.TextField(blank=True)
    robustness_score = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=7, help_text="Hex color code, e.g., #FFFFFF")
    observations = models.ManyToManyField(
        "observations.Observation", blank=True, related_name="final_clusters"
    )
    defining_forces = models.ManyToManyField(
        "clustering.DefiningForce", blank=True, related_name="final_clusters"
    )

    def __str__(self):
        return f"[Final] {self.name}"


class ClusterProposal(models.Model):
    period = models.ForeignKey(
        "scan_periods.Period", on_delete=models.CASCADE, related_name="proposals"
    )
    proposer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="proposals"
    )
    name = models.CharField(max_length=100)
    motivation = models.TextField(blank=True)
    color = models.CharField(max_length=7, help_text="Hex color code, e.g., #FFFFFF")
    observations = models.ManyToManyField(
        "observations.Observation", blank=True, related_name="proposals"
    )

    def __str__(self):
        return f"Proposal '{self.name}' by {self.proposer.username}"
