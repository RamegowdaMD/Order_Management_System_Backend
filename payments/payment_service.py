import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripePaymentService:

    @staticmethod
    def create_checkout_session(order):
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': f'Order #{order.id}',
                        },
                        'unit_amount': int(order.total_price * 100),
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:8000/api/payments/success/',
            cancel_url='http://localhost:8000/api/payments/cancel/',
            metadata={
                "order_id": order.id
            }
        )
        return session

