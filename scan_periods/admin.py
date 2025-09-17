from django.contrib import admin
from .models import Period


class PeriodAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Period model.
    """

    list_display = ("name", "status", "start_date", "end_date")
    list_filter = ("status",)


admin.site.register(Period, PeriodAdmin)
