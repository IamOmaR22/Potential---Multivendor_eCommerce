from django.contrib import admin
from .models import Product, Cart, CartItem, Order, DailyData, OrderItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price', 'quantity', 'seller')
    search_fields = ['name', 'seller__username']

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'user', 'created_at', 'updated_at')
    inlines = [CartItemInline]

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'created_at', 'total_amount', 'order_status', 'payment_method')
    search_fields = ['user__username', 'shipping_address']
    inlines = [OrderItemInline]

class DailyDataAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_revenue')

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(DailyData, DailyDataAdmin)
