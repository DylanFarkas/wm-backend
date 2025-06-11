from django.urls import include, path
from rest_framework import routers
from products import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryView, 'categories')

urlpatterns = [
    path('api/', include(router.urls)),
]