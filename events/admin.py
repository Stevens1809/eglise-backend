from django.contrib import admin
from .models import Event, EventTarget, Announcement


class EventTargetInline(admin.TabularInline):
    model = EventTarget
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["titre", "date_debut", "visibilite", "department", "cree_par"]
    list_filter = ["visibilite", "department"]
    inlines = [EventTargetInline]


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["titre", "cible", "rayon", "department", "date_publication"]
    list_filter = ["cible"]
