from django.urls import path
from .views import (
    SalesSummaryView,
    TopSellingProductsView,
    OrdersByStatusView,
    TopCustomersView,
    LowStockVariantsView,
)

urlpatterns = [
    path("sales-summary/", SalesSummaryView.as_view()),
    path("top-products/", TopSellingProductsView.as_view()),
    path("orders-by-status/", OrdersByStatusView.as_view()),
    path("top-customers/", TopCustomersView.as_view()),
    path("low-stock/", LowStockVariantsView.as_view()),
]