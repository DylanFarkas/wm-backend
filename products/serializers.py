from rest_framework import serializers
from .models import Category, Product, Productvariant, ProductImage, ProductSize

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']
        
class ProductSizeSerializer(serializers.ModelSerializer):
    variant_detail = serializers.StringRelatedField(source='variant', read_only=True)
    class Meta:
        model = ProductSize
        fields = ['id', 'size','variant', 'variant_detail', 'stock']
        
class ProductVariantSerializer(serializers.ModelSerializer):
    sizes = ProductSizeSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Productvariant
        fields = ['id', 'color', 'product', 'sizes', 'images']   
          
class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # o usa `PrimaryKeyRelatedField` si prefieres
    category_detail = serializers.StringRelatedField(source='category', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'discount', 'price',
            'is_active', 'created_at', 'category', 'category_detail', 'variants'
        ]    