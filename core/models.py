from django.conf import settings
from django.db import models


class Department(models.Model):
    """Départements administratifs et de service de l'église."""

    class Nom(models.TextChoices):
        ACCUEIL = "accueil", "Accueil"
        MEDIA = "media", "Média"
        CHORALE = "chorale", "Chorale"
        CONSISTOIRE = "consistoire", "Consistoire"
        INTERCESSION = "intercession", "Intercession"
        FEMME_FAMILLE = "femme_famille", "Services Femme et Famille"
        CAS_SOCIAL = "cas_social", "Commission Cas Social"

    nom = models.CharField(max_length=32, choices=Nom.choices, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_nom_display()


class DepartmentMembership(models.Model):
    class RoleDept(models.TextChoices):
        MEMBRE = "membre", "Membre"
        RESPONSABLE = "responsable", "Responsable"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="departements"
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="membres_dept"
    )
    role_dans_departement = models.CharField(
        max_length=16, choices=RoleDept.choices, default=RoleDept.MEMBRE
    )
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "department")

    def __str__(self):
        return f"{self.user} - {self.department} ({self.role_dans_departement})"


class Rayon(models.Model):
    """
    Un rayon = un quartier où se tiennent les prières matinales
    (lundi, mercredi, samedi) chez les fidèles.
    """

    nom = models.CharField(max_length=64, unique=True)
    chef_rayon = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rayons_diriges",
    )
    quartier_reference = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nom


class PrayerMeeting(models.Model):
    """Instance concrète d'une réunion de prière matinale pour un rayon donné."""

    class Statut(models.TextChoices):
        PREVUE = "prevue", "Prévue"
        CONFIRMEE = "confirmee", "Confirmée"
        ANNULEE = "annulee", "Annulée"

    rayon = models.ForeignKey(Rayon, on_delete=models.CASCADE, related_name="reunions")
    date = models.DateField()
    lieu = models.CharField(
        max_length=255, help_text="Adresse / nom du fidèle qui reçoit la réunion."
    )
    statut = models.CharField(
        max_length=16, choices=Statut.choices, default=Statut.PREVUE
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]
        unique_together = ("rayon", "date")

    def __str__(self):
        return f"{self.rayon} - {self.date} ({self.statut})"


class Attendance(models.Model):
    """Pointage de présence à une réunion de prière, fait par le chef de rayon."""

    prayer_meeting = models.ForeignKey(
        PrayerMeeting, on_delete=models.CASCADE, related_name="presences"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    present = models.BooleanField(default=True)
    enregistre_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="presences_enregistrees",
    )
    date_enregistrement = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("prayer_meeting", "user")

    def __str__(self):
        return f"{self.user} @ {self.prayer_meeting} - {'présent' if self.present else 'absent'}"
