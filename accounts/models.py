# accounts/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        CONTRIBUTOR = "CONTRIBUTOR", "Contributor"
        DB_ADMIN = "DB_ADMIN", "DBAdmin"  # Changed from ADMIN
        SUPER_ADMIN = "SUPER_ADMIN", "SuperAdmin"  # Changed from SUPERADMIN

    # The comments were moved outside the function calls here
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="customuser_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="customuser_permissions",
        related_query_name="user",
    )

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.CONTRIBUTOR,  # <-- This is now corrected
    )
