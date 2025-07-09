from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Productvariant, ProductSize

class OrderItemSerializer(serializers.ModelSerializer):
    variant_name = serializers.CharField(source='variant.__str__', read_only=True)
    size = serializers.CharField(source='size.size', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'variant', 'variant_name', 'size', 'quantity', 'price', 'subtotal']
     
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    customer_name = serializers.SerializerMethodField()
    customer_email = serializers.EmailField(source='user.email', read_only=True)
    customer_phone = serializers.CharField(source='user.phone_number', read_only=True)
    
    def get_customer_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'status', 'status_display', 'total_price', 'created_at',
            'items', 'address', 'department', 'city',
            'customer_name', 'customer_email', 'customer_phone'
        ]
        read_only_fields = [
            'user', 'total_price', 'created_at', 'items', 'address', 'department', 'city',
            'customer_name', 'customer_email', 'customer_phone'
        ]
     
        
class OrderCreateSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)
    department = serializers.CharField(max_length=50)
    city = serializers.CharField(max_length=50)

    def create(self, validated_data):
        user = self.context['request'].user
        cart = user.cart

        if not cart.items.exists():
            raise serializers.ValidationError("Tu carrito está vacío.")

        order = Order.objects.create(
            user=user,
            status='PENDING',
            address=validated_data['address'],
            department=validated_data['department'],
            city=validated_data['city'],
        )

        total = 0
        for item in cart.items.all():
            price = item.variant.final_price
            subtotal = price * item.quantity

            OrderItem.objects.create(
                order=order,
                variant=item.variant,
                size=item.size,
                quantity=item.quantity,
                price=price,
                subtotal=subtotal
            )

            item.size.stock -= item.quantity
            item.size.save()
            total += subtotal

        order.total_price = total
        order.save()

        cart.items.all().delete()

        return order

    def to_representation(self, instance):
        return OrderSerializer(instance).data
