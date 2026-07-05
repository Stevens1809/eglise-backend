from rest_framework import serializers
from .models import PrayerRequest


class PrayerRequestSerializer(serializers.ModelSerializer):
    department_nom = serializers.CharField(source="department.get_nom_display", read_only=True)

    class Meta:
        model = PrayerRequest
        fields = [
            "id", "user", "contenu", "department", "department_nom",
            "statut", "date_creation",
        ]
        read_only_fields = ["user", "date_creation"]
