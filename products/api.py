from rest_framework import serializers, viewsets
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
