import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from scan_periods.models import Period
from observations.models import Observation
from clustering.models import ClusterProposal, FinalCluster, DefiningForce

class Command(BaseCommand):
    help = 'Populates the database with a full set of sample data reflecting the new model structure.'

    def handle(self, *args, **kwargs):
        self.stdout.write("--- Deleting old data ---")
        # Delete in an order that respects dependencies
        Observation.objects.all().delete()
        ClusterProposal.objects.all().delete()
        FinalCluster.objects.all().delete()
        DefiningForce.objects.all().delete()
        Period.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()

        self.stdout.write("--- Creating new sample data ---")

        # --- Create a Period ---
        self.stdout.write("Creating a sample period...")
        today = date.today()
        period = Period.objects.create(
            name=f"Analysis Period - {today.strftime('%B %Y')}",
            start_date=today - timedelta(days=30),
            end_date=today,
            status='MEETING' # Set to meeting so we can see all data types
        )

        # --- Create Users ---
        self.stdout.write("Creating users...")
        user1 = CustomUser.objects.create_user(username='contrib1', password='password123', role='CONTRIBUTOR')
        user2 = CustomUser.objects.create_user(username='contrib2', password='password123', role='CONTRIBUTOR')
        user3 = CustomUser.objects.create_user(username='participant1', password='password123', role='CONTRIBUTOR')
        admin_user = CustomUser.objects.create_user(username='dbadmin1', password='password123', role='DB_ADMIN', is_staff=True)
        
        # --- Assign temporary roles for the period ---
        period.participants.add(user1, user3)
        period.db_admins.add(admin_user)

        contributors = [user1, user2, user3]
        participants = [user1, user3]

        # --- Create Observations for the Period ---
        self.stdout.write("Creating observations...")
        created_observations = []
        for i in range(20):
            author = random.choice(contributors)
            observation = Observation.objects.create(
                period=period,
                author=author,
                title=f"Sample Observation {i+1}",
                implications=f"The key implication of Obs {i+1} is...",
                type=random.choice(list(Observation.ObservationType)),
                source_link=f"http://example.com/source/{i+1}",
                interest_reason=f"This is the interesting reason for observation number {i+1}.",
                tags=random.choice(["AI", "Security", "Tech", "Future", "Innovation"]),
                status='APPROVED' # Make most approved for visibility
            )
            created_observations.append(observation)

        # --- Create Cluster Proposals from Participants ---
        self.stdout.write("Creating cluster proposals...")
        proposal1 = ClusterProposal.objects.create(
            period=period, proposer=user1, name="Participant 1's AI Proposal", 
            motivation="My take on the AI signals.", color="#FF5733"
        )
        proposal1.observations.set(random.sample(created_observations, k=4))

        proposal2 = ClusterProposal.objects.create(
            period=period, proposer=user3, name="Participant 2's Security View",
            motivation="Connecting the security dots.", color="#4A90E2"
        )
        proposal2.observations.set(random.sample(created_observations, k=5))

        # --- Create Final Clusters and Defining Forces by the DBAdmin ---
        self.stdout.write("Creating final clusters and defining forces...")
        force1 = DefiningForce.objects.create(period=period, name="The Rise of Automation", description="Automation is impacting all sectors.")
        
        final_cluster1 = FinalCluster.objects.create(
            period=period, name="Consolidated AI Trends", motivation="Outcome of the meeting.",
            robustness_score=85, color="#C70039"
        )
        final_cluster1.observations.set(random.sample(created_observations, k=6))
        final_cluster1.defining_forces.add(force1)

        self.stdout.write(self.style.SUCCESS("✓ Successfully populated the database with new structured data!"))

