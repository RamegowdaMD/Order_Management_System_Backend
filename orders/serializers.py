from rest_framework import serializers
from .models import Order , OrderItem

class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model= OrderItem
        fields= '__all__'
        read_only_fields = ['price']


class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializers(many = True, read_only = True)
    class Meta:
        model = Order
        fields= '__all__'
        read_only_fields = ['total_price','created_at','user']




