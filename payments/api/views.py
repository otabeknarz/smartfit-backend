from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings

from courses.models import Enrollment
from payments.models import Payment, Order
from smartfit import settings


@api_view(["POST"])
@permission_classes([AllowAny])
def payme_payment_view(request):
    method = request.data.get("method")
    if method == "CheckPerformTransaction":
        params = request.data.get("params", {})
        amount = params.get("amount") / 100
        order_id = params.get("account", {}).get("order_id")
        order = Order.objects.filter(id=order_id).first()

        if order and order.all_amount == amount:
            return Response({"result": {"allow": True}}, headers=settings.HEADERS)
        else:
            return Response(
                {"result": {"allow": False}}, status=400, headers=settings.HEADERS
            )

    elif method == "CreateTransaction":
        params = request.data.get("params", {})
        amount = params.get("amount") / 100
        order_id = params.get("account", {}).get("order_id")

        order = Order.objects.filter(id=order_id).first()

        if order and order.all_amount == amount:
            transaction_id = params.get("transaction_id")
            create_time = params.get("time")
            Payment.objects.create(
                user=order.user,
                amount=amount,
                method=Payment.PaymentMethodChoices.PAYME,
                transaction_id=transaction_id,
                order=order,
                time=str(create_time),
                description="",
            )
            return Response(
                {
                    "result": {
                        "create_time": create_time,
                        "transaction": transaction_id,
                        "state": 1,
                    }
                },
                headers=settings.HEADERS,
            )
        else:
            return Response({"result": {"allow": False}}, headers=settings.HEADERS)

    elif method == "PerformTransaction":
        params = request.data.get("params", {})
        transaction_id = params.get("id")
        payment = Payment.objects.filter(transaction_id=transaction_id).first()

        if payment:
            payment.mark_completed()
            order = payment.order

            enrollments = [
                Enrollment(course=course, student=payment.user)
                for course in order.courses.all()
            ]

            Enrollment.objects.bulk_create(enrollments)
            return Response(
                {
                    "result": {
                        "id": transaction_id,
                        "perform_time": int(payment.updated_at.timestamp() * 1000),
                        "state": 2,
                    }
                },
                headers=settings.HEADERS,
            )
        else:
            return Response(
                {"result": {"error": False}}, status=400, headers=settings.HEADERS
            )

    else:
        return Response(
            {"result": {"error": False}}, status=400, headers=settings.HEADERS
        )
