from django.contrib import admin
from .models import Department, DepartmentMembership, Rayon, PrayerMeeting, Attendance


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["nom"]


@admin.register(DepartmentMembership)
class DepartmentMembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "department", "role_dans_departement", "date_ajout"]
    list_filter = ["department", "role_dans_departement"]


@admin.register(Rayon)
class RayonAdmin(admin.ModelAdmin):
    list_display = ["nom", "chef_rayon", "quartier_reference"]


@admin.register(PrayerMeeting)
class PrayerMeetingAdmin(admin.ModelAdmin):
    list_display = ["rayon", "date", "lieu", "statut"]
    list_filter = ["rayon", "statut"]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["user", "prayer_meeting", "present"]
    list_filter = ["present"]
