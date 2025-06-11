from django.urls import include, path
from rest_framework import routers
from products import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet, 'categories')
router.register(r'products', views.ProductViewSet, 'products')
router.register(r'variants', views.ProductVariantViewSet, 'variants')
router.register(r'sizes', views.ProductSizeViewSet, 'sizes')
router.register(r'images', views.ProductImageViewSet, 'images')

urlpatterns = [
    path('api/', include(router.urls)),
]