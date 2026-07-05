from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventTargetViewSet, AnnouncementViewSet

router = DefaultRouter()
router.register("evenements", EventViewSet, basename="evenement")
router.register("cibles-evenement", EventTargetViewSet, basename="cible-evenement")
router.register("annonces", AnnouncementViewSet, basename="annonce")

urlpatterns = router.urls
