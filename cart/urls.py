from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet, 'cart')
router.register(r'items', CartItemViewSet, 'cart-items')

urlpatterns = [
    path('api/', include(router.urls)),
]
