from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["titre", "user", "type", "lu", "date_envoi"]
    list_filter = ["type", "lu"]
