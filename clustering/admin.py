from django.contrib import admin
from .models import ClusterProposal, FinalCluster, DefiningForce


class ClusterProposalAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Cluster Proposals.
    """

    list_display = ("name", "proposer", "period")
    list_filter = ("period",)


class FinalClusterAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Final Clusters.
    """

    list_display = ("name", "period", "robustness_score")
    list_filter = ("period",)


admin.site.register(ClusterProposal, ClusterProposalAdmin)
admin.site.register(FinalCluster, FinalClusterAdmin)
admin.site.register(DefiningForce)
