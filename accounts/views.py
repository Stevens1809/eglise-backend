from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdminConsistoire
from .serializers import UserSerializer, RegisterSerializer, FCMTokenSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Inscription libre d'un fidèle (rôle 'fidele' par défaut)."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    """Profil de l'utilisateur connecté."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpdateFCMTokenView(APIView):
    """Endpoint appelé par l'app mobile pour enregistrer/rafraîchir le token push."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FCMTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.fcm_token = serializer.validated_data["fcm_token"]
        request.user.save(update_fields=["fcm_token"])
        return Response({"status": "ok"})


class UserViewSet(viewsets.ModelViewSet):
    """
    Gestion des utilisateurs : réservé à l'Admin/Consistoire
    (création de comptes, changement de rôle, affectation à un rayon).
    Un Chef de rayon peut lister (lecture seule) les membres de SON rayon
    via l'endpoint dédié RayonMembersView (voir app core).
    """
    queryset = User.objects.all().select_related("rayon")
    serializer_class = UserSerializer
    permission_classes = [IsAdminConsistoire]
    filterset_fields = ["role", "rayon"]
