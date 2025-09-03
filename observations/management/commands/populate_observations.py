import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from accounts.models import CustomUser
from observations.models import Observation
from clustering.models import ClusterProposal, FinalCluster, DefiningForce
from scan_periods.models import Period


class Command(BaseCommand):
    help = "Populates the database with a rich set of sample data reflecting the new process."

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        # Delete in an order that respects foreign key constraints
        ClusterProposal.objects.all().delete()
        FinalCluster.objects.all().delete()
        DefiningForce.objects.all().delete()
        Observation.objects.all().delete()
        Period.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating new sample data...")

        # --- Create Users ---
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
            username="dbadmin1", password="password123", role="DB_ADMIN", is_staff=True
        )

        # --- Create a Period ---
        today = timezone.now().date()
        period = Period.objects.create(
            name=f"Scan Period - {today.strftime('%B %Y')}",
            start_date=today - timedelta(days=30),
            end_date=today,
            status="CLUSTERING",  # Set to clustering for testing
        )

        # --- Assign Roles for the Period ---
        # This is the corrected part. We now use the 'participants' variable.
        participants = [participant1, dbadmin1]
        period.participants.set(participants)
        period.db_admins.set([dbadmin1])

        # --- Create Observations for the Period ---
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
                status="APPROVED",  # Make all approved for easy testing
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated the database with improved test data!"
            )
        )
