from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from django.db import transaction


def get_or_create_cart(user):
    return Cart.objects.get_or_create(user=user)[0]

def add_product_to_cart(user, product_id, quantity=1):
    cart = get_or_create_cart(user)
    product = Product.objects.get(pk=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()
    return item

def remove_product_from_cart(user, product_id):
    cart = get_or_create_cart(user)
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()

def calculate_cart_total(user):
    cart = get_or_create_cart(user)
    total = 0
    for item in cart.items.select_related('product'):
        total += item.product.price * item.quantity
    return total

@transaction.atomic
def create_order_from_cart(user, full_name, address):
    cart = get_or_create_cart(user)
    order = Order.objects.create(
        user=user,
        full_name=full_name,
        address=address,
        paid=False
    )
    for item in cart.items.select_related('product'):
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price # capture price at checkout
        )
    cart.items.all().delete() # clear cart
    return order
