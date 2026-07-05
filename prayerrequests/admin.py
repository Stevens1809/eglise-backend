from django.contrib import admin
from .models import PrayerRequest


@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "department", "statut", "date_creation"]
    list_filter = ["department", "statut"]
