from rest_framework import serializers
from payments.models import Payment, Order


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


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class CreatePaymentSerializer(serializers.Serializer):
    course_id = serializers.CharField(required=True)
