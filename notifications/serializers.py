from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "titre", "message", "type", "lu", "date_envoi"]
        read_only_fields = ["titre", "message", "type", "date_envoi"]
