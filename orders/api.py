from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .services import get_or_create_cart, add_product_to_cart, remove_product_from_cart, calculate_cart_total, create_order_from_cart
from .models import CartItem
from products.models import Product


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    cart = get_or_create_cart(request.user)
    items = cart.items.select_related('product')
    data = [{
        'product_id': item.product.id,
        'product_name': item.product.name,
        'price': item.product.price,
        'quantity': item.quantity,
        'subtotal': item.quantity * item.product.price
    } for item in items]
    return Response({
        'items': data,
        'total': calculate_cart_total(request.user)
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))

    if not Product.objects.filter(pk=product_id).exists():
        return Response({'error': 'Product not found'}, status=404)
    
    item = add_product_to_cart(request.user, product_id, quantity)
    return Response({'message': f'Added {item.quantity} x {item.product.name} to cart.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    product_id = request.data.get('product_id')

    if not Product.objects.filter(pk=product_id).exists():
        return Response({'error': 'Product not found'}, status=404)
    
    remove_product_from_cart(request.user, product_id)
    return Response({'message': 'Product removed from cart.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    try:
        order = create_order_from_cart(request.user, full_name="Test User", address="Test Address")
        return Response({
            'message': 'Order created successfully.',
            'order_id': order.id,
            'created_at': order.created_at
        }, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
