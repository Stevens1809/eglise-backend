from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    rayon_nom = serializers.CharField(source="rayon.nom", read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "last_name", "email", "telephone",
            "role", "rayon", "rayon_nom", "fcm_token", "date_inscription", "actif",
        ]
        read_only_fields = ["id", "date_inscription"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            "username", "password", "first_name", "last_name",
            "email", "telephone", "rayon",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        # Un nouvel inscrit est toujours "fidèle" par défaut.
        # C'est un admin qui promeut ensuite (chef de rayon, resp. département).
        user.role = User.Role.FIDELE
        user.save()
        return user


class FCMTokenSerializer(serializers.Serializer):
    fcm_token = serializers.CharField()
