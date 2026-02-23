from django.urls import path
from .views import  StripeWebhookView, PaymentSuccessView, PaymentCancelView

urlpatterns = [
    path("stripe/webhook/", StripeWebhookView.as_view(), name="stripe-webhook"),
    path('success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
]

