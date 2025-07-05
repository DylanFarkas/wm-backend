from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        variant = serializer.validated_data['variant']
        size = serializer.validated_data['size']
        quantity = serializer.validated_data['quantity']

        # Validar stock
        if quantity > size.stock:
            raise ValidationError(f"Solo hay {size.stock} unidades disponibles para esta talla.")

        serializer.save(cart=cart)

    def perform_update(self, serializer):
        quantity = serializer.validated_data.get('quantity')
        size = serializer.instance.size  # ya existe, no cambiará

        # Validar stock
        if quantity > size.stock:
            raise ValidationError(f"Solo hay {size.stock} unidades disponibles para esta talla.")

        serializer.save()


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)