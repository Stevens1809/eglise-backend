from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.permissions import IsAdminConsistoire, ReadOnlyOrAdmin
from accounts.serializers import UserSerializer
from .models import Department, DepartmentMembership, Rayon, PrayerMeeting, Attendance
from .serializers import (
    DepartmentSerializer, DepartmentMembershipSerializer, RayonSerializer,
    PrayerMeetingSerializer, AttendanceSerializer,
)

User = get_user_model()


class DepartmentViewSet(viewsets.ModelViewSet):
    """Lecture pour tous, écriture réservée à l'Admin/Consistoire."""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [ReadOnlyOrAdmin]


class DepartmentMembershipViewSet(viewsets.ModelViewSet):
    queryset = DepartmentMembership.objects.select_related("user", "department")
    serializer_class = DepartmentMembershipSerializer
    permission_classes = [IsAdminConsistoire]
    filterset_fields = ["department", "user"]


class RayonViewSet(viewsets.ModelViewSet):
    """
    Lecture pour tous les authentifiés (un fidèle doit voir la liste des rayons).
    Écriture (création/suppression de rayon, changement de chef) réservée à l'Admin.
    """
    queryset = Rayon.objects.select_related("chef_rayon")
    serializer_class = RayonSerializer
    permission_classes = [ReadOnlyOrAdmin]

    @action(detail=True, methods=["get"])
    def membres(self, request, pk=None):
        """
        Liste des membres du rayon.
        Visible par : l'admin, le chef de ce rayon, et les membres du rayon eux-mêmes
        (lecture seule pour ces derniers).
        """
        rayon = self.get_object()
        user = request.user
        est_autorise = (
            user.is_admin_consistoire
            or (user.is_chef_rayon and rayon.chef_rayon_id == user.id)
            or user.rayon_id == rayon.id
        )
        if not est_autorise:
            return Response({"detail": "Non autorisé."}, status=403)
        membres = User.objects.filter(rayon=rayon)
        return Response(UserSerializer(membres, many=True).data)

    @action(detail=True, methods=["post"])
    def ajouter_membre(self, request, pk=None):
        """Le chef de rayon (ou l'admin) rattache un fidèle existant à ce rayon."""
        rayon = self.get_object()
        user = request.user
        if not (user.is_admin_consistoire or (user.is_chef_rayon and rayon.chef_rayon_id == user.id)):
            return Response({"detail": "Non autorisé."}, status=403)
        user_id = request.data.get("user_id")
        try:
            membre = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=404)
        membre.rayon = rayon
        membre.save(update_fields=["rayon"])
        return Response(UserSerializer(membre).data)

    @action(detail=True, methods=["post"])
    def retirer_membre(self, request, pk=None):
        """Le chef de rayon (ou l'admin) détache un fidèle de ce rayon."""
        rayon = self.get_object()
        user = request.user
        if not (user.is_admin_consistoire or (user.is_chef_rayon and rayon.chef_rayon_id == user.id)):
            return Response({"detail": "Non autorisé."}, status=403)
        user_id = request.data.get("user_id")
        User.objects.filter(pk=user_id, rayon=rayon).update(rayon=None)
        return Response({"status": "ok"})


class PrayerMeetingViewSet(viewsets.ModelViewSet):
    """
    - Un fidèle voit seulement les réunions de SON rayon (lecture seule).
    - Un chef de rayon peut modifier/annuler les réunions de SON rayon.
    - L'admin voit et modifie tout.
    """
    serializer_class = PrayerMeetingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["rayon", "statut", "date"]

    def get_queryset(self):
        user = self.request.user
        qs = PrayerMeeting.objects.select_related("rayon")
        if user.is_admin_consistoire:
            return qs
        if user.is_chef_rayon:
            return qs.filter(rayon__chef_rayon=user)
        # fidèle : uniquement les réunions de son propre rayon
        return qs.filter(rayon=user.rayon) if user.rayon_id else qs.none()

    def perform_update(self, serializer):
        # Sécurité supplémentaire : un chef de rayon ne peut modifier
        # que les réunions de son propre rayon.
        instance = self.get_object()
        user = self.request.user
        if not user.is_admin_consistoire and instance.rayon.chef_rayon_id != user.id:
            raise permissions.exceptions.PermissionDenied("Ce n'est pas votre rayon.")
        serializer.save()


class AttendanceViewSet(viewsets.ModelViewSet):
    """Pointage de présence : réservé au chef du rayon concerné (et à l'admin)."""
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["prayer_meeting", "user"]

    def get_queryset(self):
        user = self.request.user
        qs = Attendance.objects.select_related("user", "prayer_meeting__rayon")
        if user.is_admin_consistoire:
            return qs
        if user.is_chef_rayon:
            return qs.filter(prayer_meeting__rayon__chef_rayon=user)
        # un fidèle ne voit que son propre historique de présence
        return qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(enregistre_par=self.request.user)
