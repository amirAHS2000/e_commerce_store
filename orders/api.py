from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .services import get_or_create_cart, add_product_to_cart, remove_product_from_cart, calculate_cart_total, create_order_from_cart
from .models import CartItem
from products.models import Product
from .serializers import CartItemSerializer, AddToCartSerializer, RemoveFromCartSerializer, CheckoutSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(cart_items, many=True)
    return Response({
        'items': serializer.data,
        'total': calculate_cart_total(cart_items)
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    serializer = AddToCartSerializer(data=request.data)
    if serializer.is_valid():
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({'message': 'Product added to cart.'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    serializer = RemoveFromCartSerializer(data=request.data)
    if serializer.is_valid():
        product_id = serializer.validated_data['product_id']

        try:
            cart_item = CartItem.objects.get(
                user=request.user,
                product_id=product_id
            )
            cart_item.delete()
            return Response({'message': 'Item removed from cart.'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    serializer = CheckoutSerializer(data=request.data)
    if serializer.is_valid():
        full_name = serializer.validated_data['full_name']
        address = serializer.validated_data['address']

        try:
            order = create_order_from_cart(request.user, full_name, address)
            return Response({
                'message': 'Order created successfully.',
                'order_id': order.id,
                'created_at': order.created_at
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
