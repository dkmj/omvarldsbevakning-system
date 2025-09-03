# observations/management/commands/populate_observations.py

import random
from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from observations.models import Observation
from clustering.models import Cluster


class Command(BaseCommand):
    help = (
        "Populates the database with a richer set of sample observations and clusters."
    )

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        Observation.objects.all().delete()
        Cluster.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating new sample data...")

        # Create users
        user1 = CustomUser.objects.create_user(
            username="contrib1", password="password123", role="CONTRIBUTOR"
        )
        user2 = CustomUser.objects.create_user(
            username="contrib2", password="password123", role="CONTRIBUTOR"
        )
        user3 = CustomUser.objects.create_user(
            username="dbadmin1", password="password123", role="DB_ADMIN", is_staff=True
        )
        users = [user1, user2, user3]  # <-- user3 is now included

        # Create clusters
        cluster1 = Cluster.objects.create(
            name="AI Advancements",
            motivation="New developments in AI/ML.",
            robustness_score=80,
            color="#FF5733",
        )
        cluster2 = Cluster.objects.create(
            name="Cybersecurity Threats",
            motivation="Emerging threats and vulnerabilities.",
            robustness_score=95,
            color="#C70039",
        )
        cluster3 = Cluster.objects.create(
            name="Sustainable Tech",
            motivation="Innovations in green technology.",
            robustness_score=60,
            color="#DAF7A6",
        )
        cluster4 = Cluster.objects.create(
            name="Quantum Computing",
            motivation="Early signals in quantum space.",
            robustness_score=30,
            color="#4A90E2",
        )
        clusters = [cluster1, cluster2, cluster3, cluster4]

        # Create observations
        for i in range(20):
            author = random.choice(users)
            observation = Observation.objects.create(
                author=author,
                title=f"Sample Observation {i + 1}",
                source_link=f"http://example.com/source/{i + 1}",
                interest_reason=f"This is the interesting reason for observation number {i + 1}. It discusses a key development.",
                tags=random.choice(["AI", "Security", "Tech", "Future", "Innovation"]),
                status=random.choice(["PENDING", "APPROVED", "UNCERTAIN", "APPROVED"]),
            )

            num_clusters = random.randint(1, 2)
            if i % 3 == 0:
                num_clusters = random.randint(2, 3)

            if num_clusters > len(clusters):
                num_clusters = len(clusters)

            assigned_clusters = random.sample(clusters, num_clusters)
            observation.clusters.set(assigned_clusters)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated the database with improved test data!"
            )
        )
