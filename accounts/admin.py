"""Admin-konfiguration för appen `accounts`."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Admin configuration for the CustomUser model.

    Inherits from Django's UserAdmin and customizes the list display.

    Attributes:
        model (CustomUser): The model this admin class is for.
        list_display (list): Fields to display in the admin list view.
    """

    model = CustomUser
    # Add the 'role' field to the list display in the admin
    list_display = ["username", "email", "role", "is_staff"]


admin.site.register(CustomUser, CustomUserAdmin)
