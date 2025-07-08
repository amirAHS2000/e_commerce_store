from rest_framework import serializers
from .models import CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


class CheckoutSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=255)
