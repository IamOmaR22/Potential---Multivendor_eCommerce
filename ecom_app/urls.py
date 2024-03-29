from django.urls import path
from .views import (
    ProductCreateAPIView, ProductListAPIView, ProductDetailAPIView,
    CartListAPIView, CartDetailAPIView, CartItemCreateAPIView,
    OrderListAPIView, OrderDetailAPIView,
    DailyDataListAPIView, DailyDataDetailAPIView, CartItemListAPIView, ProductListTemplateView, api_documentation
)

urlpatterns = [
    path('products/', ProductCreateAPIView.as_view(), name='product-create'),
    path('products-list/', ProductListAPIView.as_view(), name='product-list'),
    path('products-list2/', ProductListTemplateView.as_view(), name='product-list-template'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),

    path('carts/', CartListAPIView.as_view(), name='cart-list'),
    path('carts/<int:pk>/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('cart-items/', CartItemCreateAPIView.as_view(), name='cartitem-create'),
    path('cartitem-list/', CartItemListAPIView.as_view(), name='cartitem-list'),

    path('orders/', OrderListAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),

    path('dailydata/', DailyDataListAPIView.as_view(), name='dailydata-list'),
    path('dailydata/<int:pk>/', DailyDataDetailAPIView.as_view(), name='dailydata-detail'),


    path('api_documentation/', api_documentation, name='api-documentation'),
]
