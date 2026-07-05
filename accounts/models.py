from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Utilisateur de l'application.
    Le rôle détermine le niveau d'autorisation global.
    Un utilisateur peut EN PLUS être responsable d'un rayon (chef_rayon_du)
    ou membre de départements (via DepartmentMembership dans l'app core).
    """

    class Role(models.TextChoices):
        FIDELE = "fidele", "Fidèle"
        CHEF_RAYON = "chef_rayon", "Chef de rayon"
        RESPONSABLE_DEPARTEMENT = "resp_departement", "Responsable de département"
        ADMIN_CONSISTOIRE = "admin_consistoire", "Administrateur / Consistoire"

    role = models.CharField(max_length=32, choices=Role.choices, default=Role.FIDELE)
    telephone = models.CharField(max_length=20, blank=True)
    rayon = models.ForeignKey(
        "core.Rayon",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="membres",
    )
    fcm_token = models.CharField(
        max_length=255, blank=True,
        help_text="Token Firebase Cloud Messaging pour les notifications push."
    )
    date_inscription = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_admin_consistoire(self):
        return self.role == self.Role.ADMIN_CONSISTOIRE or self.is_superuser

    @property
    def is_chef_rayon(self):
        return self.role == self.Role.CHEF_RAYON

    @property
    def is_responsable_departement(self):
        return self.role == self.Role.RESPONSABLE_DEPARTEMENT
