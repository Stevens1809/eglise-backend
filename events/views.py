from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, permissions

from notifications.services import envoyer_notification_masse
from .models import Event, EventTarget, Announcement
from .serializers import EventSerializer, EventTargetSerializer, AnnouncementSerializer

User = get_user_model()


class EventViewSet(viewsets.ModelViewSet):
    """
    Calendrier des événements. Chaque utilisateur ne voit QUE ce qui le concerne :
    - les événements 'tous'
    - les événements ciblant SON rayon
    - les événements ciblant un département dont il est membre
    L'admin/consistoire voit tout, sans filtrage.
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["visibilite", "department"]

    def get_queryset(self):
        user = self.request.user
        qs = Event.objects.select_related("department").prefetch_related("cibles")
        if user.is_admin_consistoire:
            return qs.order_by("date_debut")

        mes_departements = user.departements.values_list("department_id", flat=True)
        qs = qs.filter(
            Q(visibilite=Event.Visibilite.TOUS)
            | Q(cibles__rayon_id=user.rayon_id, visibilite=Event.Visibilite.RAYON)
            | Q(cibles__department_id__in=mes_departements, visibilite=Event.Visibilite.DEPARTEMENT)
        ).distinct()
        return qs.order_by("date_debut")

    def perform_create(self, serializer):
        user = self.request.user
        # Seuls Admin, Chef de rayon (pour son rayon) et Responsables de département
        # (pour leur département) peuvent créer un événement. Contrôle fin fait ici
        # plutôt que via une permission générique, car ça dépend du contenu envoyé.
        event = serializer.save(cree_par=user)

        # Notifie immédiatement les personnes concernées (best-effort, non bloquant).
        if event.visibilite == Event.Visibilite.TOUS:
            cibles_users = User.objects.filter(actif=True)
        else:
            cibles_users = User.objects.none()
        if cibles_users.exists():
            envoyer_notification_masse(
                cibles_users, f"Nouvel événement : {event.titre}",
                event.description or "Voir les détails dans l'app.",
                type_notif="evenement",
            )


class EventTargetViewSet(viewsets.ModelViewSet):
    queryset = EventTarget.objects.select_related("event", "rayon", "department")
    serializer_class = EventTargetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["event", "rayon", "department"]

    def perform_create(self, serializer):
        target = serializer.save()
        # Notifie les membres du rayon ou du département ciblé.
        if target.rayon_id:
            users = User.objects.filter(rayon_id=target.rayon_id, actif=True)
        elif target.department_id:
            users = User.objects.filter(
                departements__department_id=target.department_id, actif=True
            )
        else:
            users = User.objects.none()
        if users.exists():
            envoyer_notification_masse(
                users, f"Nouvel événement : {target.event.titre}",
                target.event.description or "Voir les détails dans l'app.",
                type_notif="evenement",
            )


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    Annonces. Filtrage identique à Event : un fidèle voit le global,
    celles de son rayon, et celles de ses départements.
    """
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["cible", "rayon", "department"]

    def get_queryset(self):
        user = self.request.user
        qs = Announcement.objects.select_related("auteur", "rayon", "department")
        if user.is_admin_consistoire:
            return qs

        mes_departements = user.departements.values_list("department_id", flat=True)
        return qs.filter(
            Q(cible=Announcement.Cible.GLOBAL)
            | Q(cible=Announcement.Cible.RAYON, rayon_id=user.rayon_id)
            | Q(cible=Announcement.Cible.DEPARTEMENT, department_id__in=mes_departements)
        )

    def perform_create(self, serializer):
        user = self.request.user
        announcement = serializer.save(auteur=user)

        if announcement.cible == Announcement.Cible.GLOBAL:
            users = User.objects.filter(actif=True)
        elif announcement.cible == Announcement.Cible.RAYON and announcement.rayon_id:
            users = User.objects.filter(rayon_id=announcement.rayon_id, actif=True)
        elif announcement.cible == Announcement.Cible.DEPARTEMENT and announcement.department_id:
            users = User.objects.filter(
                departements__department_id=announcement.department_id, actif=True
            )
        else:
            users = User.objects.none()

        if users.exists():
            envoyer_notification_masse(
                users, f"Annonce : {announcement.titre}", announcement.contenu,
                type_notif="annonce",
            )
