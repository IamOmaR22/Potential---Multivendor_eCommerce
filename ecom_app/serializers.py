from rest_framework import serializers
from .models import Product, Cart, CartItem, Order, OrderItem, DailyData

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'description', 'price', 'quantity', 'seller']
        read_only_fields = ['seller']

    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'cart', 'product', 'quantity']
        read_only_fields = ['cart']

    def to_representation(self, instance):
        data = super().to_representation(instance)
    
        if 'cart' in data and isinstance(data['cart'], dict):
            data['cart'].pop('items', None)
        return data

    def validate(self, data):
        return data

    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['user']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not instance.items.exists():
            data['detail'] = "Cart is empty. Add items to the cart before creating an order."
        return data


class OrderItemSerializer(serializers.ModelSerializer):
    cart_item_details = CartItemSerializer(source='cart_item', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['order_item_id', 'order', 'cart_item', 'quantity', 'cart_item_details']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True, source='items')

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].user.cart.items.count() == 0:
            raise serializers.ValidationError("Cart is empty. Add items to the cart before creating an order.")

        return data


class DailyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyData
        fields = '__all__'
