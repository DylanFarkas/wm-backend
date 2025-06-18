from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializer, ProductImageSerializer, ProductSizeSerializer, ProductVariantSerializer, ProductSerializer
from .models import Category, Product, Productvariant, ProductSize, ProductImage

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    def get_queryset(self):
        if self.action == 'list':
            return Category.objects.filter(parent__isnull=True)
        return Category.objects.all()
    
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductVariantViewSet(viewsets.ModelViewSet):
    serializer_class = ProductVariantSerializer
    queryset = Productvariant.objects.all()

class ProductSizeViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSizeSerializer
    queryset = ProductSize.objects.all()
    
class ProductImageViewSet(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()