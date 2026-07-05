from django.conf import settings
from django.db import models


class Notification(models.Model):
    """Log des notifications envoyées à un utilisateur (historique + statut lu)."""

    class Type(models.TextChoices):
        ANNONCE = "annonce", "Annonce"
        EVENEMENT = "evenement", "Événement"
        RAPPEL_PRIERE = "rappel_priere", "Rappel de prière"
        AUTRE = "autre", "Autre"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    titre = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.AUTRE)
    lu = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_envoi"]

    def __str__(self):
        return f"{self.titre} -> {self.user}"
