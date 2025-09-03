from django.views.generic import TemplateView
from clustering.models import FinalCluster
from observations.models import Observation  # Corrected import


class ReportView(TemplateView):
    template_name = "reporting/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # NOTE: This logic will need to be updated later to filter by a specific period.
        # For now, it gets all final clusters.
        context["clusters"] = FinalCluster.objects.prefetch_related(
            "observations__author"  # Also prefetch the author for efficiency
        ).all()

        # Get all approved observations that are not in any final cluster
        context["unclustered_observations"] = Observation.objects.filter(
            status="APPROVED", final_clusters__isnull=True
        )
        return context
