from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, DepartmentMembershipViewSet, RayonViewSet,
    PrayerMeetingViewSet, AttendanceViewSet,
)

router = DefaultRouter()
router.register("departements", DepartmentViewSet, basename="departement")
router.register("adhesions-departement", DepartmentMembershipViewSet, basename="adhesion-departement")
router.register("rayons", RayonViewSet, basename="rayon")
router.register("reunions-priere", PrayerMeetingViewSet, basename="reunion-priere")
router.register("presences", AttendanceViewSet, basename="presence")

urlpatterns = router.urls
