from rest_framework import serializers
from .models import Orers, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product','quantity_requested']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model =Order
        fields= ['id', 'status', 'created_at', 'items']