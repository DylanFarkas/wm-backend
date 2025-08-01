from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=user).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'checkout':
            return OrderCreateSerializer
        return OrderSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        previous_status = instance.status
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_order = serializer.save()

        # Si el estado cambió a 'CANCELLED' y no estaba antes así
        if updated_order.status == 'CANCELLED' and previous_status != 'CANCELLED':
            for item in updated_order.items.all():
                item.size.stock += item.quantity
                item.size.save()

        return Response(self.get_serializer(updated_order).data)

    @action(detail=False, methods=['post'], url_path='checkout')
    def checkout(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)