"""Database models for the clustering app."""

from django.db import models
from django.conf import settings


class DefiningForce(models.Model):
    """Representerar en drivkraft (Defining Force) inom en analysperiod.

    Dessa är nyckeldrivkrafter eller trender som identifieras under analysen
    och kan kopplas till slutgiltiga kluster.
    """

    # Use a string reference ('app_name.ModelName') to avoid circular imports
    period = models.ForeignKey(
        "scan_periods.Period", on_delete=models.CASCADE, related_name="defining_forces"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        """Returnerar en strängrepresentation av modellen.

        Returns:
            str: Namnet på drivkraften.
        """
        return self.name


class FinalCluster(models.Model):
    """Represents a final, consolidated cluster for an analysis period.

    This model is typically managed by administrators and represents the
    concluded result of grouping various observations and proposals.
    """

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
        """Returnerar en strängrepresentation av modellen.

        Returns:
            str: En formaterad sträng som indikerar att det är ett slutgiltigt
                kluster och dess namn.
        """
        return f"[Final] {self.name}"


class ClusterProposal(models.Model):
    """Represents a user-submitted proposal for a cluster.

    Users (proposers) can create their own cluster proposals, grouping a set of
    observations together with a motivation. These can later be used to form
    FinalClusters.
    """

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
        """Returnerar en strängrepresentation av modellen.

        Returns:
            str: En formaterad sträng med förslagets namn och förslagsställarens
                användarnamn.
        """
        return f"Proposal '{self.name}' by {self.proposer.username}"
