from rest_framework import serializers
from .models import Product, Cart, CartItem, Order, OrderItem, DailyData

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['unique_id', 'name', 'description', 'price', 'quantity', 'seller']
        read_only_fields = ['seller']

    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['user']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def create(self, validated_data):
        # Assuming you have a user field in your CartItem model
        user = self.context['request'].user
        validated_data['user'] = user

        return super().create(validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class DailyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyData
        fields = '__all__'
