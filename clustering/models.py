# clustering/models.py

from django.db import models


class Cluster(models.Model):
    name = models.CharField(max_length=100)
    motivation = models.TextField(blank=True)
    robustness_score = models.PositiveIntegerField(default=0)
    # Each cluster will be represented by a color
    color = models.CharField(max_length=7, help_text="Hex color code, e.g., #FFFFFF")

    def __str__(self):
        return self.name
