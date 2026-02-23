from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import stripe
from rest_framework import status
from .models import Payment
from orders.models import Order
from notifications.tasks import send_notification_task

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeWebhookView(APIView):
    permission_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
        except Exception:
            return Response(status=400)

        if event["type"] == "checkout.session.completed":

            session = event["data"]["object"]
            order_id = session["metadata"]["order_id"]

            payment = Payment.objects.get(transaction_id=session["id"])
            order = Order.objects.get(id=order_id)

            payment.payment_status = "SUCCESS"
            payment.save()

            order.status = "CONFIRMED"
            order.save()

            send_notification_task.delay(
                user_id=order.user.id,
                notification_type="PAYMENT_SUCCESS",
                message=f"Payment successful for order #{order.id}",
                email=order.user.email
            )

        return Response(status=200)


class PaymentSuccessView(APIView):
    permission_classes = []

    def get(self, request):
        return Response({"message": "Payment successful"})


class PaymentCancelView(APIView):
    permission_classes = []

    def get(self, request):
        return Response({"message": "Payment cancelled"})


