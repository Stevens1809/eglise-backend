"""
Permissions custom DRF reflétant les 4 niveaux d'autorisation :
Administrateur/Consistoire > Chef de rayon > Responsable de département > Fidèle.
"""
from rest_framework import permissions


class IsAdminConsistoire(permissions.BasePermission):
    """Autorise uniquement le Consistoire / Administrateur (accès total)."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_admin_consistoire
        )


class IsChefDeSonRayon(permissions.BasePermission):
    """
    Autorise le chef d'un rayon à agir uniquement sur SON rayon
    (ou l'admin, qui a accès à tout).
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_admin_consistoire:
            return True
        # obj peut être un Rayon, ou tout objet avec un attribut .rayon
        rayon = obj if obj.__class__.__name__ == "Rayon" else getattr(obj, "rayon", None)
        return bool(
            user.is_chef_rayon and rayon is not None and rayon.chef_rayon_id == user.id
        )


class IsResponsableDeSonDepartement(permissions.BasePermission):
    """Autorise le responsable d'un département à agir sur SON département."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_admin_consistoire:
            return True
        department = (
            obj if obj.__class__.__name__ == "Department" else getattr(obj, "department", None)
        )
        if department is None:
            return False
        from core.models import DepartmentMembership
        return DepartmentMembership.objects.filter(
            user=user, department=department,
            role_dans_departement=DepartmentMembership.RoleDept.RESPONSABLE,
        ).exists()


class ReadOnlyOrAdmin(permissions.BasePermission):
    """Lecture pour tous les authentifiés, écriture réservée à l'admin/consistoire."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_authenticated and request.user.is_admin_consistoire)
