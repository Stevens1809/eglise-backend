from django.conf import settings
from django.db import models


class PrayerRequest(models.Model):
    """Demande de prière ou signalement de cas social, adressé à un département."""

    class Statut(models.TextChoices):
        NOUVEAU = "nouveau", "Nouveau"
        EN_COURS = "en_cours", "En cours"
        TRAITE = "traite", "Traité"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="demandes",
        help_text="Peut être vide si la demande est anonyme."
    )
    contenu = models.TextField()
    department = models.ForeignKey(
        "core.Department", on_delete=models.SET_NULL, null=True,
        related_name="demandes_recues"
    )
    statut = models.CharField(
        max_length=16, choices=Statut.choices, default=Statut.NOUVEAU
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return f"Demande #{self.id} -> {self.department}"
