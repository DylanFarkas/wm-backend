from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAppAdmin
from django.utils.dateparse import parse_date
from django.db.models import Sum
from orders.models import Order, OrderItem
from products.models import ProductSize, Productvariant
from django.db.models import Count
from django.contrib.auth import get_user_model

# Create your views here.

class SalesSummaryView(APIView):
    permission_classes = [IsAppAdmin]

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not start_date or not end_date:
            return Response({"error": "Parámetros 'start_date' y 'end_date' son requeridos."}, status=400)

        start = parse_date(start_date)
        end = parse_date(end_date)

        if not start or not end:
            return Response({"error": "Formato de fecha inválido. Usa YYYY-MM-DD."}, status=400)

        orders = Order.objects.filter(created_at__date__gte=start, created_at__date__lte=end, status__in=['PAID', 'SHIPPED'])

        total_orders = orders.count()
        total_income = orders.aggregate(total=Sum('total_price'))['total'] or 0

        total_products = OrderItem.objects.filter(order__in=orders).aggregate(
            total=Sum('quantity')
        )['total'] or 0

        return Response({
            "start_date": start_date,
            "end_date": end_date,
            "total_orders": total_orders,
            "total_income": float(total_income),
            "total_products_sold": total_products,
        })
        
class TopSellingProductsView(APIView):
    permission_classes = [IsAppAdmin]

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not start_date or not end_date:
            return Response({"error": "Parámetros 'start_date' y 'end_date' son requeridos."}, status=400)

        start = parse_date(start_date)
        end = parse_date(end_date)

        if not start or not end:
            return Response({"error": "Formato de fecha inválido. Usa YYYY-MM-DD."}, status=400)

        # Filtrar órdenes por fecha
        orders = Order.objects.filter(created_at__date__gte=start, created_at__date__lte=end, status__in=['PAID', 'SHIPPED'])

        # Filtrar OrderItems por esas órdenes
        order_items = OrderItem.objects.filter(order__in=orders)

        # Agrupar por variante y sumar cantidades
        top_variants = order_items.values(
            'variant__id',
            'variant__product__name',
            'variant__color',
            'size__size'
        ).annotate(
            total_sold=Sum('quantity')
        ).order_by('-total_sold')[:10]  # top 10

        return Response(list(top_variants))
    
class OrdersByStatusView(APIView):
    permission_classes = [IsAppAdmin]

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not start_date or not end_date:
            return Response({"error": "Parámetros 'start_date' y 'end_date' son requeridos."}, status=400)

        start = parse_date(start_date)
        end = parse_date(end_date)

        if not start or not end:
            return Response({"error": "Formato de fecha inválido. Usa YYYY-MM-DD."}, status=400)

        orders = Order.objects.filter(created_at__date__gte=start, created_at__date__lte=end, status__in=['PAID', 'SHIPPED', 'PENDING', 'CANCELLED'])

        counts = orders.values('status').annotate(total=Count('id'))

        return Response(list(counts))
    
User = get_user_model()

class TopCustomersView(APIView):
    permission_classes = [IsAppAdmin]

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not start_date or not end_date:
            return Response({"error": "Parámetros 'start_date' y 'end_date' son requeridos."}, status=400)

        start = parse_date(start_date)
        end = parse_date(end_date)

        if not start or not end:
            return Response({"error": "Formato de fecha inválido. Usa YYYY-MM-DD."}, status=400)

        orders = Order.objects.filter(created_at__date__gte=start, created_at__date__lte=end, status__in=['PAID', 'SHIPPED'])

        top_customers = orders.values(
            'user__id', 'user__email', 'user__name',
        ).annotate(
            total_spent=Sum('total_price'),
            orders_count=Count('id')
        ).order_by('-total_spent')[:10]

        return Response(list(top_customers))
    
class LowStockVariantsView(APIView):
    permission_classes = [IsAppAdmin]

    def get(self, request):
        threshold = int(request.query_params.get('threshold', 5))  # Puedes personalizarlo desde el frontend
        low_stock_sizes = ProductSize.objects.filter(stock__lte=threshold)

        data = [
            {
                "product": size.variant.product.name,
                "variant": size.variant.color,
                "size": size.size,
                "stock": size.stock,
            }
            for size in low_stock_sizes
        ]
        return Response(data)