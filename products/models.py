from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def update_activity(self):
        # If any variant has stock, the product is active
        active = any(variant.has_stock() for variant in self.variants.all())
        self.is_active = active
        self.save()
        
    def __str__(self):
        return self.name
    
class Productvariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants',on_delete=models.CASCADE)
    color = models.CharField(max_length=20)
    
    def has_stock(self):
        return any(size.stock > 0 for size in self.sizes.all())
    
    def __str__(self):
        return f"{self.product.name} - {self.color}"
    
class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]
    
    variant = models.ForeignKey(Productvariant, related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualiza el estado del producto al cambiar el stock
        self.variant.product.update_activity()
        
    def __str__(self):
        return f"{self.variant} - {self.size} ({self.stock})"
    
    class Meta:
        unique_together = ('variant', 'size')
    
class ProductImage(models.Model):
    variant = models.ForeignKey(Productvariant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='imgs/product_images/', blank=True, null=True)
    
    def __str__(self):
        return f"Imagen de {self.variant}"