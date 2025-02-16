from rest_framework import serializers
from users.models import User, CustomSession


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "username", "phone_number", "gender", "age", "height", "date_joined")
        extra_kwargs = {
            "id": {"required": True},
        }


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomSession
        fields = ("user", "ip_address", "device_info", "last_online", "created_at")
