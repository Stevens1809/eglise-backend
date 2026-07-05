from rest_framework import serializers
from .models import Event, EventTarget, Announcement


class EventTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTarget
        fields = ["id", "event", "rayon", "department"]


class EventSerializer(serializers.ModelSerializer):
    cibles = EventTargetSerializer(many=True, read_only=True)
    department_nom = serializers.CharField(source="department.get_nom_display", read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "titre", "description", "date_debut", "date_fin", "lieu",
            "cree_par", "department", "department_nom", "visibilite",
            "date_creation", "cibles",
        ]
        read_only_fields = ["cree_par", "date_creation"]


class AnnouncementSerializer(serializers.ModelSerializer):
    auteur_nom = serializers.CharField(source="auteur.get_full_name", read_only=True)
    rayon_nom = serializers.CharField(source="rayon.nom", read_only=True)
    department_nom = serializers.CharField(source="department.get_nom_display", read_only=True)

    class Meta:
        model = Announcement
        fields = [
            "id", "titre", "contenu", "auteur", "auteur_nom", "date_publication",
            "cible", "rayon", "rayon_nom", "department", "department_nom",
        ]
        read_only_fields = ["auteur", "date_publication"]
