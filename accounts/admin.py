from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "first_name", "last_name", "role", "rayon", "actif"]
    list_filter = ["role", "rayon", "actif"]
    search_fields = ["username", "first_name", "last_name", "telephone"]
    fieldsets = UserAdmin.fieldsets + (
        ("Église", {"fields": ("role", "telephone", "rayon", "fcm_token", "actif")}),
    )
