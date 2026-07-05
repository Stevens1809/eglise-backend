from rest_framework.routers import DefaultRouter
from .views import PrayerRequestViewSet

router = DefaultRouter()
router.register("demandes-priere", PrayerRequestViewSet, basename="demande-priere")

urlpatterns = router.urls
