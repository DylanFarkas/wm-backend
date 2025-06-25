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
        fields = ['id', 'variant', 'image']
        
class ProductSizeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = ProductSize
        fields = ['id', 'size', 'stock']
        
class ProductVariantSerializer(serializers.ModelSerializer):
    sizes = ProductSizeSerializer(many=True)
    id = serializers.IntegerField(required=False)
    images = ProductImageSerializer(many=True, required=False)
    class Meta:
        model = Productvariant
        fields = ['id', 'color', 'sizes', 'images'] 
        
    def create(self, validated_data):
        sizes_data = validated_data.pop('sizes')
        variant = Productvariant.objects.create(**validated_data)
        for size_data in sizes_data:
            ProductSize.objects.create(variant=variant, **size_data)
        return variant
    
    def update(self, instance, validated_data):
        sizes_data = validated_data.pop('sizes', [])

        instance.color = validated_data.get('color', instance.color)
        instance.save()

        existing_size_ids = [size.id for size in instance.sizes.all()]
        received_size_ids = [s.get('id') for s in sizes_data if s.get('id') is not None]

        # Eliminar tallas no incluidas
        for size in instance.sizes.all():
            if size.id not in received_size_ids:
                size.delete()

        # Crear o actualizar tallas
        for size_data in sizes_data:
            size_id = size_data.get('id', None)
            if size_id:
                size = ProductSize.objects.get(id=size_id, variant=instance)
                for attr, value in size_data.items():
                    setattr(size, attr, value)
                size.save()
            else:
                ProductSize.objects.create(variant=instance, **size_data)

        return instance
          
class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()) 
    category_detail = serializers.StringRelatedField(source='category', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'discount', 'price',
            'is_active', 'created_at', 'category', 'variants',
            'category_detail'
        ]
        read_only_fields = ['is_active', 'created_at']
        
    def create(self, validated_data):
        variants_data = validated_data.pop('variants', [])

        # Crear el producto
        product = Product.objects.create(**validated_data)

        # Crear las variantes y sus tallas
        for variant_data in variants_data:
            sizes_data = variant_data.pop('sizes', [])
            variant = Productvariant.objects.create(product=product, **variant_data)
            for size_data in sizes_data:
                ProductSize.objects.create(variant=variant, **size_data)

        return product
        
    def update(self, instance, validated_data):
        variants_data = validated_data.pop('variants', [])

        # Actualiza campos del producto
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        existing_variant_ids = [v.id for v in instance.variants.all()]
        received_variant_ids = [v.get('id') for v in variants_data if v.get('id') is not None]

        # Eliminar variantes no incluidas
        for variant in instance.variants.all():
            if variant.id not in received_variant_ids:
                variant.delete()

        # Crear o actualizar variantes
        for variant_data in variants_data:
            variant_id = variant_data.get('id', None)
            if variant_id:
                variant_instance = Productvariant.objects.get(id=variant_id, product=instance)
                variant_serializer = ProductVariantSerializer(instance=variant_instance, data=variant_data)
                variant_serializer.is_valid(raise_exception=True)
                variant_serializer.save()
            else:
                variant_serializer = ProductVariantSerializer(data=variant_data)
                variant_serializer.is_valid(raise_exception=True)
                variant_serializer.save(product=instance)

        instance.update_activity()
        return instance