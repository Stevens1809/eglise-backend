from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    Chaque utilisateur ne voit QUE ses propres notifications.
    Champ 'lu' modifiable par l'utilisateur (marquer comme lu),
    le reste est en lecture seule (les notifs sont créées côté serveur).
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
