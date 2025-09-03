# reporting/views.py


from django.views.generic import TemplateView

from clustering.models import Cluster
from observations.models import Observation


class ReportView(TemplateView):
    template_name = "reporting/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all clusters and pre-fetch their approved observations
        # to make the database query more efficient.
        context["clusters"] = (
            Cluster.objects.prefetch_related(
                "observations",
            )
            .filter(
                observations__status="APPROVED",
            )
            .distinct()
        )

        # Get all approved observations that are not in any cluster
        context["unclustered_observations"] = Observation.objects.filter(
            status="APPROVED",
            clusters__isnull=True,
        )
        return context
