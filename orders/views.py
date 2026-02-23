from django.shortcuts import render
from .models import Order
from .models import OrderItem
from rest_framework import generics,permissions
from .serializers import OrderSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Product
from rest_framework import status
from payments.payment_service import StripePaymentService
from payments.models import Payment
from django.db import transaction
from payments.dto import PaymentData
from notifications.tasks import send_notification_task

class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializers
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailEach(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializers
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class AddProductToOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        user = request.user
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity",1)) # idu default value if use does not send any quantity 

        try:
            product = Product.objects.get(id = product_id)
        except Product.DoesNotExist:
            return Response({"error":"Product not found"},status=404)


        #idu pending order tagolake exist idre
        order = Order.objects.filter(user = user , status = 'PENDING').first()


        # idu to create new if not there
        if not order:
            order  = Order.objects.create(
                user = user,
                status = 'PENDING',
                address ="Not Provided"
            )

        #idu check madoke product already idre quantity update madoke

        order_item = OrderItem.objects.filter(
            order = order,
            product = product
        ).first()

        if order_item:
            order_item.quantity += quantity
            order_item.save()
        else:
            OrderItem.objects.create(
                order = order,
                product = product,
                quantity = quantity
            )
        return Response({"message": "Product added successfully"},
        status =  status.HTTP_201_CREATED
        )

class PlaceOrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        address = request.data.get("address")
        payment_method = request.data.get("payment_method")

        if not address or not payment_method:
            return Response(
                {"error": "Address and payment method are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.filter(
            user=request.user,
            status='PENDING'
        ).first()

        if not order or order.items.count() == 0:
            return Response(
                {"error": "Order has no items"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            
            if payment_method == "COD":

                payment_data = PaymentData(
                    order_id=order.id,
                    amount=order.total_price,
                    payment_method="COD"
                )

                payment = Payment.objects.create(
                    order_id=payment_data.order_id,
                    amount=payment_data.amount,
                    payment_method=payment_data.payment_method,
                    payment_status=payment_data.payment_status
                )

                order.status = "CONFIRMED"
                order.address = address
                order.save()

                send_notification_task.delay(
                    user_id=request.user.id,
                    notification_type="PAYMENT_SUCCESS",
                    message=f"Order #{order.id} placed successfully (COD)",
                    email=request.user.email
                )

                return Response({
                    "message": "Order placed successfully (Cash on Delivery)",
                    "order_id": order.id,
                    "payment_status": payment.payment_status
                })

            
            if payment_method == "STRIPE":

                session = StripePaymentService.create_checkout_session(order)

                payment_data = PaymentData(
                    order_id=order.id,
                    amount=order.total_price,
                    payment_method="STRIPE",
                    transaction_id=session.id
                )

                payment = Payment.objects.create(
                    order_id=payment_data.order_id,
                    amount=payment_data.amount,
                    payment_method=payment_data.payment_method,
                    payment_status=payment_data.payment_status,
                    transaction_id=payment_data.transaction_id
                )

                order.address = address
                order.save()

                return Response({
                    "checkout_url": session.url,
                    "session_id": session.id
                })

        return Response(
            {"error": "Invalid payment method"},
            status=status.HTTP_400_BAD_REQUEST
        )
