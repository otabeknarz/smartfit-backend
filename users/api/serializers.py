from rest_framework import serializers
from users.models import User, CustomSession, OnboardingAnswers

from payments.api.serializers import PaymentSerializer


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "picture",
            "gender",
        )


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "picture",
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


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "username")


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomSession
        fields = ("user", "ip_address", "device_info", "last_online", "created_at")


class OnboardingAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingAnswers
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
