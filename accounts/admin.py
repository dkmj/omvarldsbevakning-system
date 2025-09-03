# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add the 'role' field to the list display in the admin
    list_display = ["username", "email", "role", "is_staff"]


admin.site.register(CustomUser, CustomUserAdmin)
