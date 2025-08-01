from rest_framework import serializers
from .models import Wishlist
from products.serializers import ProductSerializer

class WishlistSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    
    class Meta:
        model = Wishlist
        fields = '__all__'
        read_only_fields = ['user']
