import time
from unittest import case

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from decimal import Decimal
from payments.models import Payment


@method_decorator(csrf_exempt, name="dispatch")
class PaymeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        method = data.get("method")
        params = data.get("params", {})
        request_id = data.get("id")

        handler = {
            "CheckPerformTransaction": self.check_perform_transaction,
            "CreateTransaction": self.create_transaction,
            "PerformTransaction": self.perform_transaction,
            "CheckTransaction": self.check_transaction,
            "CancelTransaction": self.cancel_transaction,
        }.get(method)

        if handler:
            return handler(params, request_id)

        return Response({
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Method not found"},
            "id": request_id
        })

    def check_perform_transaction(self, params, request_id):
        try:
            print("CheckPerformTransaction called with params:", params)
            payment_id = params["account"]["payment_id"]
            amount = Decimal(params["amount"]) / 100
            print("Parsed payment_id:", payment_id, "amount:", amount)

            payment = get_object_or_404(Payment, id=payment_id)
            print("Found payment:", payment)

            if payment.status != Payment.StatusChoices.PENDING:
                return self.error_response(-31050, "Transaction already processed", request_id)

            if amount != payment.amount:
                return self.error_response(-31001, f"Incorrect amount: expected {payment.amount}, got {amount}",
                                           request_id)

            return self.success_response({"allow": True}, request_id)

        except Exception as e:
            print("Error in check_perform_transaction:", str(e))
            return self.error_response(-31099, "Error in checking transaction", request_id)

    def create_transaction(self, params, request_id):
        try:
            payment_id = params["account"]["payment_id"]
            payme_transaction_id = params["id"]
            payment = get_object_or_404(Payment, id=payment_id)

            if payment.transaction_id and payment.transaction_id != payme_transaction_id:
                return self.error_response(-31008, "Transaction already exists", request_id)

            payment.transaction_id = payme_transaction_id
            payment.save()

            return self.success_response({
                "create_time": int(time.time() * 1000),
                "transaction": payme_transaction_id,
                "state": 1,
                "receivers": None,
            }, request_id)

        except Exception:
            return self.error_response(-31099, "Failed to create transaction", request_id)

    def perform_transaction(self, params, request_id):
        try:
            transaction_id = params["id"]
            payment = get_object_or_404(Payment, transaction_id=transaction_id)

            if payment.status == Payment.StatusChoices.COMPLETED:
                return self.success_response({
                    "transaction": transaction_id,
                    "perform_time": int(payment.updated_at.timestamp() * 1000),
                    "state": 2,
                }, request_id)

            payment.mark_completed()

            return self.success_response({
                "transaction": transaction_id,
                "perform_time": int(payment.updated_at.timestamp() * 1000),
                "state": 2,
            }, request_id)

        except Exception:
            return self.error_response(-31099, "Failed to perform transaction", request_id)

    def check_transaction(self, params, request_id):
        try:
            transaction_id = params["id"]
            payment = get_object_or_404(Payment, transaction_id=transaction_id)

            state = 2 if payment.status == Payment.StatusChoices.COMPLETED else 1

            return self.success_response({
                "transaction": transaction_id,
                "create_time": int(payment.created_at.timestamp() * 1000),
                "perform_time": int(payment.updated_at.timestamp() * 1000),
                "cancel_time": 0,
                "reason": None,
                "state": state,
            }, request_id)

        except Exception:
            return self.error_response(-31099, "Transaction not found", request_id)

    def cancel_transaction(self, params, request_id):
        try:
            transaction_id = params["id"]
            reason = params.get("reason", 0)
            payment = get_object_or_404(Payment, transaction_id=transaction_id)

            payment.mark_failed()

            return self.success_response({
                "transaction": transaction_id,
                "cancel_time": int(payment.updated_at.timestamp() * 1000),
                "state": -1,
                "reason": reason,
            }, request_id)

        except Exception:
            return self.error_response(-31099, "Failed to cancel transaction", request_id)

    def success_response(self, result, request_id):
        return Response({
            "jsonrpc": "2.0",
            "result": result,
            "id": request_id
        })

    def error_response(self, code, message, request_id):
        return Response({
            "jsonrpc": "2.0",
            "error": {
                "code": code,
                "message": message,
                "data": message,
            },
            "id": request_id
        })
