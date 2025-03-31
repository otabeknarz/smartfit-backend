from rest_framework import serializers
from users.models import User, CustomSession, Payment


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "gender",
        )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "amount",
            "currency",
            "status",
            "created_at",
        )


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "username",
            "phone_number",
            "gender",
            "age",
            "height",
            "date_joined",
            "payments",
        )
        extra_kwargs = {
            "id": {"required": True},
        }


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomSession
        fields = ("user", "ip_address", "device_info", "last_online", "created_at")
