from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom configuration for the User model in the Django admin.
    """

    # This copies the default fields from the standard UserAdmin...
    fieldsets = UserAdmin.fieldsets + (
        # ...and adds our custom 'Role' section.
        (
            "Application Role",
            {
                "fields": ("role",),
            },
        ),
    )

    # This controls the columns displayed in the user list view.
    list_display = ["username", "email", "role", "is_staff"]


admin.site.register(CustomUser, CustomUserAdmin)
