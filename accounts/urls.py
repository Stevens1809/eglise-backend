from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, MeView, UpdateFCMTokenView, UserViewSet

router = DefaultRouter()
router.register("utilisateurs", UserViewSet, basename="utilisateur")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path("me/fcm-token/", UpdateFCMTokenView.as_view(), name="fcm-token"),
] + router.urls
