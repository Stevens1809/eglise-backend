from rest_framework import viewsets, permissions
from core.models import DepartmentMembership
from .models import PrayerRequest
from .serializers import PrayerRequestSerializer


class PrayerRequestViewSet(viewsets.ModelViewSet):
    """
    - Un fidèle crée des demandes et ne voit QUE les siennes.
    - Un responsable de département voit les demandes adressées à SON département.
    - L'admin voit tout.
    """
    serializer_class = PrayerRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["department", "statut"]

    def get_queryset(self):
        user = self.request.user
        qs = PrayerRequest.objects.select_related("user", "department")
        if user.is_admin_consistoire:
            return qs
        mes_departements_geres = DepartmentMembership.objects.filter(
            user=user, role_dans_departement=DepartmentMembership.RoleDept.RESPONSABLE
        ).values_list("department_id", flat=True)
        if mes_departements_geres:
            return qs.filter(department_id__in=mes_departements_geres) | qs.filter(user=user)
        return qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
