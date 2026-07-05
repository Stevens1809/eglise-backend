from rest_framework import serializers
from .models import Department, DepartmentMembership, Rayon, PrayerMeeting, Attendance


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "nom", "description"]


class DepartmentMembershipSerializer(serializers.ModelSerializer):
    user_nom = serializers.CharField(source="user.get_full_name", read_only=True)
    department_nom = serializers.CharField(source="department.get_nom_display", read_only=True)

    class Meta:
        model = DepartmentMembership
        fields = [
            "id", "user", "user_nom", "department", "department_nom",
            "role_dans_departement", "date_ajout",
        ]


class RayonSerializer(serializers.ModelSerializer):
    chef_rayon_nom = serializers.CharField(source="chef_rayon.get_full_name", read_only=True)
    nombre_membres = serializers.SerializerMethodField()

    class Meta:
        model = Rayon
        fields = [
            "id", "nom", "chef_rayon", "chef_rayon_nom",
            "quartier_reference", "nombre_membres",
        ]

    def get_nombre_membres(self, obj):
        return obj.membres.count()


class PrayerMeetingSerializer(serializers.ModelSerializer):
    rayon_nom = serializers.CharField(source="rayon.nom", read_only=True)
    taux_presence = serializers.SerializerMethodField()

    class Meta:
        model = PrayerMeeting
        fields = [
            "id", "rayon", "rayon_nom", "date", "lieu", "statut",
            "notes", "taux_presence",
        ]

    def get_taux_presence(self, obj):
        total = obj.presences.count()
        if not total:
            return None
        presents = obj.presences.filter(present=True).count()
        return round(100 * presents / total, 1)


class AttendanceSerializer(serializers.ModelSerializer):
    user_nom = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = Attendance
        fields = [
            "id", "prayer_meeting", "user", "user_nom", "present",
            "enregistre_par", "date_enregistrement",
        ]
        read_only_fields = ["enregistre_par", "date_enregistrement"]
