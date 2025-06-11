from django.contrib import admin
from .models import Category, Product, Productvariant, ProductSize, ProductImage
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Productvariant)
admin.site.register(ProductSize)
admin.site.register(ProductImage)