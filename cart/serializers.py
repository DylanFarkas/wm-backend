from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Productvariant, ProductSize
from products.serializers import ProductVariantSerializer, ProductSizeSerializer

class CartItemSerializer(serializers.ModelSerializer):
    variant_id = serializers.PrimaryKeyRelatedField(
        queryset=Productvariant.objects.all(),
        source='variant',
        write_only=True
    )
    size_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductSize.objects.all(),
        source='size',
        write_only=True
    )

    variant = ProductVariantSerializer(read_only=True)
    size = ProductSizeSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'variant_id', 'size_id', 'variant', 'size', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items', 'total_price']
        read_only_fields = ['user', 'created_at']

    def get_total_price(self, obj):
        return obj.total_price()

