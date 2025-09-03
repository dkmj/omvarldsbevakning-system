"""
A Django management command to populate the database with sample data.

This command is designed for development purposes. It clears out existing
data (except for superusers) and creates a fresh set of users, periods,
observations, and clusters to provide a realistic testing environment for the
frontend and API.

To run this command:
    uv run python manage.py populate_observations
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
        """
        The main logic for the management command.

        This method executes the following steps in order:
        1. Deletes all existing data (respecting foreign key constraints).
        2. Creates a new set of sample users with different roles.
        3. Creates a single, active 'Period' for the current month.
        4. Assigns some users as Participants and DBAdmins for that Period.
        5. Creates a batch of sample Observations within the Period.
        """
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
        # Create a set of users with different roles for testing.
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
        # Create a single period for all the test data to belong to.
        today = timezone.now().date()
        period = Period.objects.create(
            name=f"Scan Period - {today.strftime('%B %Y')}",
            start_date=today - timedelta(days=30),
            end_date=today,
            status="CLUSTERING",  # Set to a state useful for testing the clustering UI.
        )

        # --- Section 3: Assign Roles for the Period ---
        # Designate which users will act as Participants and DBAdmins for this specific period.
        participants = [participant1, dbadmin1]
        period.participants.set(participants)
        period.db_admins.set([dbadmin1])

        # --- Section 4: Create Observations for the Period ---
        # Create a batch of observations authored by various contributors.
        for i in range(20):
            author = random.choice([user1, user2, participant1])
            Observation.objects.create(
                period=period,
                author=author,
                title=f"Sample Observation {i + 1}",
                implications=f"This could impact the future of topic {i % 4 + 1}.",
                type=random.choice([t[0] for t in Observation.ObservationType.choices]),
                interest_reason=f"This is the interesting reason for observation number {i + 1}.",
                tags=random.choice(["AI", "Security", "Tech", "Future", "Innovation"]),
                status="APPROVED",  # Make all approved for easy testing.
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated the database with improved test data!"
            )
        )
