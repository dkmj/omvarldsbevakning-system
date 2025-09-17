"""
A Django management command to populate the database with sample data.

This command clears out existing data (except for superusers) and creates a
fresh set of users, a period, observations, proposals, and final clusters
to provide a realistic testing environment.
"""

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import CustomUser
from clustering.models import ClusterProposal, DefiningForce, FinalCluster
from observations.models import Observation
from scan_periods.models import Period


class Command(BaseCommand):
    """Handles the creation of sample data for the application."""

    help = "Populates the database with a rich set of sample data reflecting the new process."

    def handle(self, *args, **kwargs):
        """The main logic for the management command."""
        self.stdout.write("Deleting old data...")
        # Delete in an order that respects foreign key constraints to avoid errors.
        ClusterProposal.objects.all().delete()
        FinalCluster.objects.all().delete()
        DefiningForce.objects.all().delete()
        Observation.objects.all().delete()
        Period.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating new sample data...")

        # --- Section 1: Create Users ---
        user1 = CustomUser.objects.create_user(
            username="contrib1", password="password123", role="CONTRIBUTOR"
        )
        user2 = CustomUser.objects.create_user(
            username="contrib2", password="password123", role="CONTRIBUTOR"
        )
        participant1 = CustomUser.objects.create_user(
            username="participant1", password="password123", role="CONTRIBUTOR"
        )
        dbadmin1 = CustomUser.objects.create_user(
            username="dbadmin1",
            password="password123",
            role="DB_ADMIN",
            is_staff=True,
        )

        # --- Section 2: Create a Period ---
        today = timezone.now().date()
        period = Period.objects.create(
            name=f"Analysis Period - {today.strftime('%B %Y')}",
            start_date=today - timedelta(days=30),
            end_date=today,
            status="MEETING",  # Set to a state useful for testing all UIs
        )

        # --- Section 3: Assign Roles for the Period ---
        period.participants.set([participant1, dbadmin1])
        period.db_admins.set([dbadmin1])

        # --- Section 4: Create Observations for the Period ---
        observations = []
        for i in range(20):
            obs = Observation.objects.create(
                period=period,
                author=random.choice([user1, user2, participant1]),
                title=f"Sample Observation {i + 1}",
                implications=f"This could impact the future of topic {i % 4 + 1}.",
                type=random.choice([t[0] for t in Observation.ObservationType.choices]),
                interest_reason=f"Reason for observation {i + 1}.",
                tags=random.choice(["AI", "Security", "Tech", "Future"]),
                status="APPROVED",
            )
            observations.append(obs)

        # --- Section 5: Create Cluster Proposals ---
        proposal1 = ClusterProposal.objects.create(
            period=period,
            proposer=participant1,
            name="Participant 1's AI Proposal",
            color="#4A90E2",
        )
        proposal1.observations.set(random.sample(observations, k=5))

        proposal2 = ClusterProposal.objects.create(
            period=period,
            proposer=dbadmin1,
            name="Admin's Security Proposal",
            color="#C70039",
        )
        proposal2.observations.set(random.sample(observations, k=5))

        # --- Section 6: Create Final Clusters and Defining Forces ---
        force1 = DefiningForce.objects.create(
            period=period,
            name="The Rise of Automation",
            description="Automation is impacting all sectors.",
        )

        final_cluster = FinalCluster.objects.create(
            period=period,
            name="Consolidated AI Trends",
            motivation="Outcome of the meeting.",
            robustness_score=85,
            color="#C70039",
        )
        final_cluster.observations.set(random.sample(observations, k=6))
        final_cluster.defining_forces.set([force1])

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated the database with improved test data!"
            )
        )
