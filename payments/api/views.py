import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from payments.models import Payment, Order


class Payme:
    class General:
        INVALID_HTTP_METHOD = (-32300, "Invalid request method. POST required.")
        PARSE_ERROR = (-32700, "Invalid JSON format.")
        INVALID_REQUEST = (
            -32600,
            "Invalid RPC request format or missing required fields.",
        )
        METHOD_NOT_FOUND = (-32601, "Requested method not found.")
        INSUFFICIENT_PRIVILEGES = (
            -32504,
            "Insufficient privileges to execute this method.",
        )
        INTERNAL_ERROR = (-32400, "Internal system error. Please try again later.")

    class Merchant:
        WRONG_AMOUNT = (
            -31001,
            "The transaction amount does not match the order amount.",
        )
        TRANSACTION_NOT_FOUND = (-31003, "Transaction not found.")
        CANNOT_CANCEL_TRANSACTION = (
            -31007,
            "The product or service is already delivered and cannot be canceled.",
        )
        OPERATION_NOT_ALLOWED = (
            -31008,
            "This operation cannot be performed with the current transaction status.",
        )
        INVALID_ACCOUNT_INPUT = (
            -31050,
            "Invalid account input. Please check your login or phone number.",
        )

    class CheckPerformTransaction:
        WRONG_AMOUNT = (-31001, "The transaction amount is incorrect.")
        INVALID_ACCOUNT_INPUT = (
            -31050,
            "Invalid buyer account input. Please verify the provided details.",
        )

        @staticmethod
        def check_perform_transaction(payment_id, amount):
            payment = Payment.objects.filter(id=payment_id).update(amount=amount)
            if not payment:
                return Payme.CheckPerformTransaction.INVALID_ACCOUNT_INPUT
            if payment.amount == amount * 100:
                return True
            else:
                return Payme.CheckPerformTransaction.WRONG_AMOUNT

    class CreateTransaction:
        WRONG_AMOUNT = (-31001, "The transaction amount is incorrect.")
        OPERATION_NOT_ALLOWED = (-31008, "This operation cannot be performed.")
        INVALID_ACCOUNT_INPUT = (
            -31050,
            "Invalid account data provided. Please check the input details.",
        )

    class PerformTransaction:
        TRANSACTION_NOT_FOUND = (-31003, "No transaction was found.")
        OPERATION_NOT_ALLOWED = (-31008, "This operation is not permitted.")
        INVALID_ACCOUNT_INPUT = (
            -31050,
            "Buyer account details are invalid.",
        )

    class CancelTransaction:
        TRANSACTION_NOT_FOUND = (-31003, "No transaction was found to cancel.")
        CANNOT_CANCEL_TRANSACTION = (
            -31007,
            "The order is complete and cannot be canceled.",
        )


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

        return Response(
            {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": "Method not found"},
                "id": request_id,
            }
        )

    def check_perform_transaction(self, params, request_id):
        try:
            order_id = params.get("account", {}).get("order_id")
            amount = float(params.get("amount", 0)) / 100

            order = Order.objects.filter(id=order_id).first()

            if not order:
                return self.error_response(
                    Payme.CheckPerformTransaction.INVALID_ACCOUNT_INPUT[0],
                    Payme.CheckPerformTransaction.INVALID_ACCOUNT_INPUT[1],
                    request_id,
                )

            if amount != float(order.all_amount):
                return self.error_response(
                    Payme.CheckPerformTransaction.WRONG_AMOUNT[0],
                    Payme.CheckPerformTransaction.WRONG_AMOUNT[1],
                    request_id,
                )

            return self.success_response({"allow": True}, request_id)

        except Exception as e:
            print("Error in check_perform_transaction:", str(e))
            return self.error_response(
                -31099, "Error in checking transaction", request_id
            )

    def create_transaction(self, params, request_id):
        try:
            order_id = params.get("account", {}).get("order_id")
            amount = float(params.get("amount", 0)) / 100
            payme_transaction_id = params.get("id")
            order = Order.objects.filter(id=order_id).first()

            if not order:
                return self.error_response(
                    Payme.CreateTransaction.INVALID_ACCOUNT_INPUT[0],
                    Payme.CreateTransaction.INVALID_ACCOUNT_INPUT[1],
                    request_id,
                )

            if amount != float(order.all_amount):
                return self.error_response(
                    Payme.CreateTransaction.WRONG_AMOUNT[0],
                    Payme.CreateTransaction.WRONG_AMOUNT[1],
                    request_id,
                )

            payment = Payment.objects.filter(transaction_id=payme_transaction_id).first()

            if not payment:
                Payment.objects.create(
                    transaction_id=payme_transaction_id,
                    amount=amount,
                    order=order,
                    user=order.user,
                    currency=Payment.CurrencyChoices.UZS,
                    method=Payment.PaymentMethodChoices.PAYME,
                )

            elif float(payment.amount) != amount:
                return self.error_response(
                    Payme.CreateTransaction.WRONG_AMOUNT[0],
                    Payme.CreateTransaction.WRONG_AMOUNT[1],
                    request_id,
                )

            else:
                state = 0
                if payment.status == Payment.StatusChoices.PENDING :
                    state = 1
                elif payment.status == Payment.StatusChoices.COMPLETED:
                    state = 2
                else:
                    state = 0

                return self.success_response(
                    {
                        "create_time": int(time.time() * 1000),
                        "transaction": payme_transaction_id,
                        "state": state,
                        "receivers": None,
                    },
                    request_id
                )


            return self.success_response(
                {
                    "create_time": int(time.time() * 1000),
                    "transaction": payme_transaction_id,
                    "state": 1,
                    "receivers": None,
                },
                request_id
            )

        except Exception:
            return self.error_response(
                -31099, "Failed to create transaction", request_id
            )

    def perform_transaction(self, params, request_id):
        try:
            transaction_id = params["id"]
            payment = get_object_or_404(Payment, transaction_id=transaction_id)

            if payment.status == Payment.StatusChoices.COMPLETED:
                return self.success_response(
                    {
                        "transaction": transaction_id,
                        "perform_time": int(payment.updated_at.timestamp() * 1000),
                        "state": 2,
                    },
                    request_id,
                )

            payment.mark_completed()

            return self.success_response(
                {
                    "transaction": transaction_id,
                    "perform_time": int(payment.updated_at.timestamp() * 1000),
                    "state": 2,
                },
                request_id,
            )

        except Exception:
            return self.error_response(
                -31099, "Failed to perform transaction", request_id
            )

    def check_transaction(self, params, request_id):
        try:
            transaction_id = params.get("id")
            payment = Payment.objects.filter(transaction_id=transaction_id).first()

            if not payment:
                return self.error_response(
                    Payme.CreateTransaction.INVALID_ACCOUNT_INPUT[0],
                    Payme.CreateTransaction.INVALID_ACCOUNT_INPUT[1],
                    request_id,
                )

            state = 2 if payment.status == Payment.StatusChoices.COMPLETED else 1

            return self.success_response(
                {
                    "transaction": transaction_id,
                    "create_time": int(payment.created_at.timestamp() * 1000),
                    "perform_time": int(payment.updated_at.timestamp() * 1000),
                    "cancel_time": 0,
                    "reason": None,
                    "state": state,
                },
                request_id,
            )

        except Exception:
            return self.error_response(-31099, "Transaction not found", request_id)

    def cancel_transaction(self, params, request_id):
        try:
            transaction_id = params["id"]
            reason = params.get("reason", 0)
            payment = get_object_or_404(Payment, transaction_id=transaction_id)

            payment.mark_failed()

            return self.success_response(
                {
                    "transaction": transaction_id,
                    "cancel_time": int(payment.updated_at.timestamp() * 1000),
                    "state": -1,
                    "reason": reason,
                },
                request_id,
            )

        except Exception:
            return self.error_response(
                -31099, "Failed to cancel transaction", request_id
            )

    @staticmethod
    def success_response(result, request_id):
        return Response(
            {"jsonrpc": "2.0", "result": result, "id": request_id}, status=200
        )

    @staticmethod
    def error_response(code, message, request_id):
        return Response(
            {
                "jsonrpc": "2.0",
                "error": {
                    "code": code,
                    "message": message,
                    "data": message,
                },
                "id": request_id,
            },
            status=400,
        )
