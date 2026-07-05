from django.conf import settings
from django.db import models


class Event(models.Model):
    """Événement général : culte spécial, activité de département, etc."""

    class Visibilite(models.TextChoices):
        TOUS = "tous", "Tous les fidèles"
        RAYON = "rayon", "Rayon(s) spécifique(s)"
        DEPARTEMENT = "departement", "Département(s) spécifique(s)"

    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField(null=True, blank=True)
    lieu = models.CharField(max_length=255, blank=True)
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="evenements_crees"
    )
    department = models.ForeignKey(
        "core.Department", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="evenements"
    )
    visibilite = models.CharField(
        max_length=16, choices=Visibilite.choices, default=Visibilite.TOUS
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_debut"]

    def __str__(self):
        return self.titre


class EventTarget(models.Model):
    """Portée de diffusion d'un événement (pour cibler les notifications)."""

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="cibles")
    rayon = models.ForeignKey(
        "core.Rayon", on_delete=models.CASCADE, null=True, blank=True
    )
    department = models.ForeignKey(
        "core.Department", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        cible = self.rayon or self.department or "?"
        return f"{self.event} -> {cible}"


class Announcement(models.Model):
    """Annonce simple (moins structurée qu'un événement calendrier)."""

    class Cible(models.TextChoices):
        GLOBAL = "global", "Toute l'église"
        RAYON = "rayon", "Un rayon"
        DEPARTEMENT = "departement", "Un département"

    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="annonces"
    )
    date_publication = models.DateTimeField(auto_now_add=True)
    cible = models.CharField(max_length=16, choices=Cible.choices, default=Cible.GLOBAL)
    rayon = models.ForeignKey(
        "core.Rayon", on_delete=models.CASCADE, null=True, blank=True
    )
    department = models.ForeignKey(
        "core.Department", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        ordering = ["-date_publication"]

    def __str__(self):
        return self.titre
