from rest_framework import serializers
from .models import Category, Product, Productvariant, ProductImage, ProductSize


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'subcategories']

    def get_subcategories(self, obj):
        subcats = obj.subcategories.all()
        return CategorySerializer(subcats, many=True).data
        
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
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()) 
    category_detail = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'discount', 'price',
            'is_active', 'created_at', 'category', 'category_detail', 'variants'
        ]    