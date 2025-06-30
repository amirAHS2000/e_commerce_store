from django.urls import path
from .api import view_cart, add_to_cart, remove_from_cart, checkout


urlpatterns = [
    path('cart/', view_cart, name='view-cart'),
    path('cart/add/', add_to_cart, name='add-to-cart'),
    path('cart/remove/', remove_from_cart, name='remove-from-cart'),
    path('order/checkout/', checkout, name='checkout'),
]
